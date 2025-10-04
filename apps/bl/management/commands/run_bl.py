from django.core.management.base import BaseCommand
from django.conf import settings
import numpy as np
from apps.bl.priors import market_equilibrium_returns
from apps.bl.combine import posterior_mean
from apps.bl.optimize import optimal_weights
from apps.bl.models import BLRun, PosteriorWeight
from apps.universe.models import Asset

class Command(BaseCommand):
    help = "Run Black–Litterman and store posterior weights"

    def add_arguments(self, parser):
        parser.add_argument("--as-of", required=True)
        parser.add_argument("--benchmark", default=settings.BL_BENCHMARK)
        parser.add_argument("--tau", type=float, default=settings.BL_TAU)
        parser.add_argument("--delta", type=float, default=settings.BL_DELTA)

    def handle(self, *args, **opts):
        # NOTE: replace these dummies with real data loads
        n = 5
        Sigma = np.eye(n) * 0.04
        w_mkt = np.ones(n) / n
        pi = market_equilibrium_returns(Sigma, w_mkt, delta=opts["delta"])

        # toy view: first asset outperforms second by 2%
        P = np.zeros((1, n)); P[0,0] = 1; P[0,1] = -1
        q = np.array([0.02])
        Omega = np.eye(1) * 0.0004

        mu = posterior_mean(Sigma, pi, P, q, Omega, tau=opts["tau"])
        w = optimal_weights(mu, Sigma)

        run = BLRun.objects.create(as_of=opts["as_of"], benchmark=opts["benchmark"],
                                   tau=opts["tau"], delta=opts["delta"], note="toy")
        assets = list(Asset.objects.all()[:n])
        # if assets < n, create dummies for demo
        while len(assets) < n:
            a = Asset.objects.create(ticker=f"ASSET{len(assets)+1}")
            assets.append(a)
        for a, wi in zip(assets, w):
            PosteriorWeight.objects.create(run=run, asset=a, weight=float(wi))

        self.stdout.write(self.style.SUCCESS(f"BL run saved (id={run.id}) with {n} weights"))
