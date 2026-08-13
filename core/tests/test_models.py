from django.test import TestCase
from decimal import Decimal
from datetime import date, timedelta

from core.models import Categoria, LancamentoFinanceiro


class CategoriaLancamentoModelTests(TestCase):
    def test_is_ativo_and_valor_normalizado(self):
        c1 = Categoria.objects.create(nome='Receita', tipo=Categoria.TIPO_ATIVO)
        c2 = Categoria.objects.create(nome='Despesa', tipo=Categoria.TIPO_PASSIVO)

        l1 = LancamentoFinanceiro.objects.create(
            descricao='R1', valor=Decimal('100.00'), categoria=c1, is_pago=False, data_vencimento=date.today()
        )
        l2 = LancamentoFinanceiro.objects.create(
            descricao='D1', valor=Decimal('50.00'), categoria=c2, is_pago=False, data_vencimento=date.today()
        )

        self.assertTrue(l1.is_ativo())
        self.assertFalse(l2.is_ativo())
        self.assertIsInstance(l1.valor_normalizado(), Decimal)


class LancamentoAdminFormTests(TestCase):
    def test_admin_form_rejects_nonpositive_and_future_paid(self):
        from core.admin import LancamentoFinanceiroAdminForm

        c = Categoria.objects.create(nome='Receita2', tipo=Categoria.TIPO_ATIVO)
        data_today = date.today()
        data_future = data_today + timedelta(days=10)

        # non-positive valor should be invalid
        form = LancamentoFinanceiroAdminForm(data={
            'descricao': 'X',
            'valor': '0.00',
            'categoria': c.pk,
            'is_pago': False,
            'data_vencimento': data_today,
        })
        self.assertFalse(form.is_valid())
        self.assertIn('valor', form.errors)

        # marking as paid before vencimento should be invalid
        form2 = LancamentoFinanceiroAdminForm(data={
            'descricao': 'Y',
            'valor': '10.00',
            'categoria': c.pk,
            'is_pago': True,
            'data_vencimento': data_future,
        })
        self.assertFalse(form2.is_valid())
        self.assertIn('__all__', form2.errors)
