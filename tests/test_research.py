import sys, unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'python'))
import research as m
import numpy as np
import pandas as pd

class HomologyTests(unittest.TestCase):
    def test_triangle_is_filled(self):
        d=np.ones((3,3))-np.eye(3)
        h0,h1=m.diagrams(d)
        self.assertEqual(len(h0),2); self.assertEqual(len(h1),0)
        np.testing.assert_allclose(h0[:,1],1)
    def test_square_loop_dies_at_diagonal(self):
        points=np.array([[0,0],[1,0],[1,1],[0,1]])
        d=np.linalg.norm(points[:,None]-points[None,:],axis=2)
        h0,h1=m.diagrams(d)
        self.assertEqual(len(h0),3);self.assertEqual(len(h1),1)
        np.testing.assert_allclose(h1[0],[1,np.sqrt(2)],atol=1e-6)
    def test_w2_diagonal_matching_and_symmetry(self):
        a=np.array([[0,2.]])
        self.assertAlmostEqual(m.wasserstein2(a,[]),np.sqrt(2))
        self.assertEqual(m.wasserstein2([],[]),0)
        self.assertEqual(m.wasserstein2(a,a),0)
        b=np.array([[.1,1.9],[1,1.2]])
        self.assertAlmostEqual(m.wasserstein2(a,b),m.wasserstein2(b,a))
    def test_correlation_distance_is_metric(self):
        r=np.random.default_rng(7).normal(size=(60,30))
        corr,d=m.metric(r)
        np.testing.assert_allclose(d,d.T);np.testing.assert_allclose(np.diag(d),0)
        for k in range(30):self.assertTrue(np.all(d<=d[:,k,None]+d[None,k,:]+1e-8))
        with self.assertRaises(ValueError):m.metric(np.ones((60,30)))
    def test_features_are_suffix_invariant(self):
        r=np.random.default_rng(2).normal(size=(155,30))
        changed=r.copy();changed[145:]*=10
        a,ac,_,_=m.rolling_features(r);b,bc,_,_=m.rolling_features(changed)
        np.testing.assert_allclose(a[:145-121],b[:145-121])
        np.testing.assert_allclose(ac[:145-121],bc[:145-121])
    def test_forward_labels_exclude_present(self):
        r=np.zeros((150,2));r[121,0]=10;r[122:127,0]=-.01
        label=m.future_target(r,0,np.array([121]),'direction')
        self.assertEqual(label[0],0)
        self.assertTrue(np.isnan(m.future_target(r,0,np.array([149]),'direction')[0]))
    def test_purge_and_scaler_past_only(self):
        origins=np.arange(121,701);train=m.split_indices(origins,400,20)
        self.assertTrue(np.all(origins[train]+20<400))
        x=np.column_stack([np.arange(580),np.ones(580)])
        model=m.fit_model(x[train],np.arange(len(train))%2,'direction')
        np.testing.assert_allclose(model[0].mean_,x[train].mean(axis=0))
    def test_backtest_future_suffix_cannot_change_earlier_prediction(self):
        rng=np.random.default_rng(1);origins=np.arange(121,701)
        x=rng.normal(size=(580,6));y=rng.integers(0,2,580).astype(float);y[-5:]=np.nan
        dates=pd.bdate_range('2020-01-01',periods=701).strftime('%Y-%m-%d').tolist()
        a=m.backtest([x,x,x],y,origins,'direction',dates)
        future_y=y.copy();future_y[400:-5]=1-y[400:-5]
        future_x=x.copy();future_x[400:]*=20
        b=m.backtest([future_x]*3,future_y,origins,'direction',dates)
        earlier=[row for row in a['rows'] if row['date']<dates[origins[400]]]
        self.assertEqual([r['predictions'] for r in earlier],[r['predictions'] for r in b['rows'][:len(earlier)]])
        for fold in a['folds']:self.assertLess(fold['labelEnd'],fold['origin'])
    def test_validation_rejects_missing_and_duplicate_dates(self):
        frame=m.demo_prices(n=600);m.validate_prices(frame)
        bad=frame.copy();bad.iloc[3,4]=np.nan
        with self.assertRaises(ValueError):m.validate_prices(bad)
        bad=frame.copy();idx=list(bad.index);idx[3]=idx[2];bad.index=idx
        with self.assertRaises(ValueError):m.validate_prices(bad)
        with self.assertRaises(ValueError):m.validate_prices(frame.iloc[:,:29])
    def test_surrogate_covariance_is_preserved(self):
        r=np.random.default_rng(4).normal(size=(175,30));s=m.shuffled_surrogate(r)
        np.testing.assert_allclose(np.cov(r,rowvar=False),np.cov(s,rowvar=False),atol=1e-12)


class ProviderTests(unittest.TestCase):
    def test_provider_duplicates_and_incomplete_sessions(self):
        from download_prices import parse_history
        dates=pd.bdate_range('2020-01-01',periods=601).strftime('%Y-%m-%d').tolist()
        data={'values':[{'datetime':d,'close':'100'} for d in dates]}
        self.assertEqual(len(parse_history(data,dates[-1])),600)
        data['values'].append(data['values'][0])
        with self.assertRaises(ValueError):parse_history(data,'2026-09-30')
        with self.assertRaises(ValueError):parse_history({'status':'error'},'2026-09-30')

if __name__=='__main__':unittest.main()
