
eID = [
  "Pt > 20",
  "CBID_MEDIUM==1",
]
muID = [
  "Pt > 20",
  "IsGlobal==1",
  "IsTracker==1",
  "MuonHits>0",
  "MatchedStations>1",
  "TkLayersWithMeasurement>5",
  "PixHits>0",
  "NormTrkChi2<10",
  "PVDXY<.2",
  "PVDZ<.5",
  "RelPFIsoDBDefault<.2"
]

ecuts = [leg+cut for leg in ("e1","e2") for cut in eID]
mcuts = [leg+cut for leg in ("m1","m2") for cut in muID]


