Meeting
=======

### COHERENT Analysis: 2025.8.28

- Sam: What is between the signal volume and the CR veto? My concern is accidentally vetoing signal events without high z shielding between the Ar and veto
  Could also use CRY for simulating cosmic muons/neutrons, which includes angle/energy dependence as well as latitude, date, …

- Andrew: Ecomug is a pretty convenient and easy to integrate event generator in a Geant simulation. Can simulate muons from arbitrary surfaces with energy/angular correlations

- Phil: So, if it’s 6 m above, and the detector is about 1 m in diameter, then even if you went out to a a plane of 12 m by 12 m, you would only be simulating half of your muons
  (Assuming a 6 m by 6 m plane, 6 m above)

- Yun-Tse: I did 10x10m^2 in my old analysis and assumed that we can easily rejected muons leaving a track > 5cm in the TPC.  The acceptance is so low and therefore I reduced the generation plane this time.  But you are right, we should expand it in the next production.  John is planning to continue this analysis in a slower pace during the school year, which allows us some time to run this big MC production 

- Janina: Do you have a lower muon energy threshold above which you can reject most of them?
