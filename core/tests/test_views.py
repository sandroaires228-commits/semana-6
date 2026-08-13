from django.test import TestCase
from django.contrib.auth.models import User, Permission
from django.urls import reverse
from datetime import date
from decimal import Decimal

from core.models import Categoria, LancamentoFinanceiro


class FinanceiroViewTests(TestCase):
    def setUp(self):
        # criar usuário staff com permissão de view
        self.staff = User.objects.create_user('staff', 's@example.com', 'pass')
        self.staff.is_staff = True
        perm = Permission.objects.get(codename='view_lancamentofinanceiro')
        self.staff.user_permissions.add(perm)
        self.staff.save()

        self.client.force_login(self.staff)

        c1 = Categoria.objects.create(nome='AtivoCat', tipo=Categoria.TIPO_ATIVO)
        c2 = Categoria.objects.create(nome='PassivoCat', tipo=Categoria.TIPO_PASSIVO)
        today = date.today()
        LancamentoFinanceiro.objects.create(descricao='A1', valor=Decimal('100.00'), categoria=c1, is_pago=False, data_vencimento=today)
        LancamentoFinanceiro.objects.create(descricao='P1', valor=Decimal('40.00'), categoria=c2, is_pago=False, data_vencimento=today)

    def test_dashboard_access_and_context(self):
        resp = self.client.get(reverse('financeiro_dashboard'))
        self.assertEqual(resp.status_code, 200)
        self.assertIn('total_ativos', resp.context)
        self.assertIn('total_passivos', resp.context)
        self.assertEqual(resp.context['total_ativos'], Decimal('100.00'))
        self.assertEqual(resp.context['total_passivos'], Decimal('40.00'))

    def test_trends_json(self):
        resp = self.client.get(reverse('financeiro_trends'))
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertIn('labels', data)
        self.assertIn('ativos', data)
        self.assertIn('passivos', data)
        self.assertEqual(sum(data['ativos']), 100.0)
        self.assertEqual(sum(data['passivos']), 40.0)

    def test_permission_denied_for_user_without_permission(self):
        u = User.objects.create_user('normal', 'n@example.com', 'pass')
        u.is_staff = True
        u.save()
        self.client.force_login(u)
        resp = self.client.get(reverse('financeiro_dashboard'))
        self.assertEqual(resp.status_code, 403)
