import flet as ft
from datetime import datetime

# ------------------ CLASSES ------------------
class Cliente:
    def __init__(self, nome, telefone, email, cliente_id):
        self.nome = nome
        self.telefone = telefone
        self.email = email
        self.cliente_id = cliente_id

class Quarto:
    def __init__(self, numero, tipo, preco, disponivel=True):
        self.numero = numero
        self.tipo = tipo
        self.preco = preco
        self.disponivel = disponivel

class Reserva:
    def __init__(self, cliente, quarto, check_in, check_out, status="Ativa"):
        self.cliente = cliente
        self.quarto = quarto
        self.check_in = check_in
        self.check_out = check_out
        self.status = status

class GerenciadorDeReservas:
    def __init__(self):
        self.clientes = []
        self.quartos = []
        self.reservas = []

    def adicionar_cliente(self, cliente):
        self.clientes.append(cliente)

    def adicionar_quarto(self, quarto):
        self.quartos.append(quarto)

    def verificar_disponibilidade(self):
        return [q for q in self.quartos if q.disponivel]

    def criar_reserva(self, cliente, quarto, check_in, check_out):
        if quarto.disponivel:
            quarto.disponivel = False
            reserva = Reserva(cliente, quarto, check_in, check_out)
            self.reservas.append(reserva)
            return reserva
        return None

    def cancelar_reserva(self, reserva):
        reserva.status = "Cancelada"
        reserva.quarto.disponivel = True

# ------------------ INTERFACE ------------------
def main(page: ft.Page):
    page.title = "Raffy Hotel - Hotel Boutique"
    page.padding = 20
    page.bgcolor = "#FFF8F0"
    page.vertical_alignment = ft.MainAxisAlignment.START

    sistema = GerenciadorDeReservas()

    # Quartos iniciais
    sistema.adicionar_quarto(Quarto(101, "Single", 250))
    sistema.adicionar_quarto(Quarto(102, "Double", 400))
    sistema.adicionar_quarto(Quarto(201, "Suite", 700))

    # ------------------ FUNÇÃO DE NAVEGAÇÃO ------------------
    def mudar_tela(e):
        page.views.clear()
        page.views.append(telas[e.control.data])
        page.update()

    # ------------------ TELA INICIAL ------------------
    def tela_inicial():
        lista_quartos = ft.Column(
            [ft.Text(f"Quarto {q.numero} - {q.tipo} - R$ {q.preco} - {'Disponível' if q.disponivel else 'Ocupado'}",
                     size=16) for q in sistema.quartos],
            spacing=10
        )

        return ft.View(
            "inicio",
            [
                ft.Text("Raffy Hotel", size=36, weight="bold", color="#D96C75"),
                ft.Text("Hotel Boutique - Sistema de Reservas", size=18, color="#555555"),
                ft.Divider(thickness=2, color="#D96C75"),
                lista_quartos,
                ft.Row([
                    ft.ElevatedButton("Realizar Reserva", data="reserva", on_click=mudar_tela, style=ft.ButtonStyle(bgcolor="#D96C75")),
                    ft.ElevatedButton("Gerenciar Clientes", data="clientes", on_click=mudar_tela, style=ft.ButtonStyle(bgcolor="#F3A683")),
                    ft.ElevatedButton("Ver Reservas", data="listar_reservas", on_click=mudar_tela, style=ft.ButtonStyle(bgcolor="#6C5B7B"))
                ], alignment="spaceAround", spacing=20)
            ]
        )

    # ------------------ GERENCIAMENTO DE CLIENTES ------------------
    def tela_clientes():
        nome = ft.TextField(label="Nome")
        telefone = ft.TextField(label="Telefone")
        email = ft.TextField(label="E-mail")
        lista_clientes = ft.Column()

        def atualizar_lista():
            lista_clientes.controls = [
                ft.Text(f"ID {c.cliente_id} - {c.nome} - {c.email}") for c in sistema.clientes
            ]
            page.update()

        def adicionar(e):
            if nome.value.strip() and email.value.strip():
                cliente = Cliente(nome.value, telefone.value, email.value, len(sistema.clientes)+1)
                sistema.adicionar_cliente(cliente)
                nome.value = telefone.value = email.value = ""
                atualizar_lista()

        atualizar_lista()

        return ft.View(
            "clientes",
            [
                ft.Text("Gerenciamento de Clientes", size=28, weight="bold", color="#D96C75"),
                nome, telefone, email,
                ft.ElevatedButton("Adicionar Cliente", on_click=adicionar, style=ft.ButtonStyle(bgcolor="#D96C75")),
                ft.Divider(),
                ft.Text("Clientes Cadastrados:", size=16),
                lista_clientes,
                ft.ElevatedButton("Voltar", data="inicio", on_click=mudar_tela, style=ft.ButtonStyle(bgcolor="#6C5B7B"))
            ]
        )

    # ------------------ FORMULÁRIO DE RESERVA ------------------
    def tela_reserva():
        clientes_dropdown = ft.Dropdown(width=250)
        quartos_dropdown = ft.Dropdown(width=250)
        check_in = ft.TextField(label="Check-in (AAAA-MM-DD)")
        check_out = ft.TextField(label="Check-out (AAAA-MM-DD)")
        mensagem = ft.Text("", color="green")

        def carregar_dados():
            clientes_dropdown.options = [ft.dropdown.Option(str(c.cliente_id), c.nome) for c in sistema.clientes]
            quartos_dropdown.options = [ft.dropdown.Option(str(q.numero), f"{q.numero} - {q.tipo}") for q in sistema.verificar_disponibilidade()]
            page.update()

        def reservar(e):
            if not clientes_dropdown.value or not quartos_dropdown.value:
                mensagem.value = "Selecione cliente e quarto!"
                page.update()
                return
            cliente_id = int(clientes_dropdown.value)
            cliente = next(c for c in sistema.clientes if c.cliente_id==cliente_id)
            quarto_num = int(quartos_dropdown.value)
            quarto = next(q for q in sistema.quartos if q.numero==quarto_num)
            reserva = sistema.criar_reserva(cliente, quarto, check_in.value, check_out.value)
            if reserva:
                mensagem.value = f"Reserva criada! Quarto {quarto.numero} para {cliente.nome}."
                carregar_dados()
            else:
                mensagem.value = "Erro: quarto indisponível."
            page.update()

        carregar_dados()

        return ft.View(
            "reserva",
            [
                ft.Text("Criar Nova Reserva", size=28, weight="bold", color="#D96C75"),
                clientes_dropdown, quartos_dropdown, check_in, check_out,
                ft.ElevatedButton("Confirmar Reserva", on_click=reservar, style=ft.ButtonStyle(bgcolor="#D96C75")),
                mensagem,
                ft.ElevatedButton("Voltar", data="inicio", on_click=mudar_tela, style=ft.ButtonStyle(bgcolor="#6C5B7B"))
            ]
        )

    # ------------------ LISTAR RESERVAS ------------------
    def tela_listar_reservas():
        lista = ft.Column()

        def atualizar():
            lista.controls = []
            for r in sistema.reservas:
                lista.controls.append(
                    ft.Row([
                        ft.Text(f"{r.cliente.nome} - Quarto {r.quarto.numero} - {r.status}", width=350),
                        ft.ElevatedButton("Cancelar", on_click=lambda e, reserva=r: cancelar(reserva), style=ft.ButtonStyle(bgcolor="#F85F73"))
                    ], alignment="spaceBetween")
                )
            page.update()

        def cancelar(reserva):
            sistema.cancelar_reserva(reserva)
            atualizar()

        atualizar()

        return ft.View(
            "listar_reservas",
            [
                ft.Text("Lista de Reservas", size=28, weight="bold", color="#D96C75"),
                lista,
                ft.ElevatedButton("Voltar", data="inicio", on_click=mudar_tela, style=ft.ButtonStyle(bgcolor="#6C5B7B"))
            ]
        )

    # ------------------ DICIONÁRIO DE TELAS ------------------
    telas = {
        "inicio": tela_inicial(),
        "clientes": tela_clientes(),
        "reserva": tela_reserva(),
        "listar_reservas": tela_listar_reservas(),
    }

    page.views.append(telas["inicio"])
    page.update()

# ------------------ RODAR APP ------------------
ft.app(target=main, view=ft.WEB_BROWSER)
