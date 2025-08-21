void plot_spectra(TString fname = "energyTimeBreakdown.root"){
  gStyle -> SetOptTitle(0);
  gStyle -> SetOptStat(0);

  TFile *f1 = new TFile(fname);

  TH1D *hPE = (TH1D*)f1 -> Get("protonEnergy");
  hPE -> SetXTitle("Proton energy at instant of #pi^{+} creation (MeV)");
  hPE -> SetYTitle("arb. units");
  hPE -> Rebin(4);
  hPE -> Scale(1.e6/hPE -> GetEntries());

  TH2D *nuMu = (TH2D*)f1 -> Get("nuMu");
  TH1D *nuMuEnergy = (TH1D*)nuMu -> ProjectionY();
  nuMuEnergy -> GetXaxis() -> SetRangeUser(0, 300);
  TH1D *nuMuTiming = (TH1D*)nuMu -> ProjectionX();
  TH2D *antiNuMu = (TH2D*)f1 -> Get("antiNuMu");
  TH1D *antiNuMuEnergy = (TH1D*)antiNuMu -> ProjectionY();
  TH1D *antiNuMuTiming = (TH1D*)antiNuMu -> ProjectionX();
  TH2D *nuE = (TH2D*)f1 -> Get("nuE");
  TH1D *nuEEnergy = (TH1D*)nuE -> ProjectionY();
  TH1D *nuETiming = (TH1D*)nuE -> ProjectionX();
  TH2D *antiNuE = (TH2D*)f1 -> Get("antiNuE");
  TH1D *antiNuEEnergy = (TH1D*)antiNuE -> ProjectionY();
  TH1D *antiNuETiming = (TH1D*)antiNuE -> ProjectionX();

  nuMuEnergy -> SetLineColor(kRed - 4);
  TH1D *nuMuEnergyC = (TH1D*)nuMuEnergy -> Clone();
  nuMuEnergyC -> SetFillColor(kRed - 4);
  
  nuEEnergy -> SetLineColor(kOrange + 1);
  nuEEnergy -> SetLineStyle(2);
  nuEEnergy -> SetLineWidth(2);
  TH1D *nuEEnergyC = (TH1D*)nuEEnergy -> Clone();
  nuEEnergyC -> SetFillColor(kOrange + 1);
  
  antiNuMuEnergy -> SetLineColor(kBlue + 1);
  antiNuMuEnergy -> SetLineStyle(3);
  antiNuMuEnergy -> SetLineWidth(2);
  TH1D *antiNuMuEnergyC = (TH1D*)antiNuMuEnergy -> Clone();
  antiNuMuEnergyC -> SetFillColor(kBlue + 1);
  
  antiNuEEnergy -> SetLineColor(kCyan + 1);
  // antiNuEEnergy -> SetLineStyle(5);
  TH1D *antiNuEEnergyC = (TH1D*)antiNuEEnergy -> Clone();
  antiNuEEnergyC -> SetFillColor(kCyan + 1);

  TH1D *hDelayed = (TH1D*)antiNuMuTiming -> Clone();
  hDelayed -> Add(nuETiming);

  nuMuTiming -> SetLineColor(kRed);
  TH1D *nuMuTimingC = (TH1D*)nuMuTiming -> Clone();
  nuMuTimingC -> SetFillColor(kRed);

  hDelayed -> SetLineColor(kBlue + 1);
  TH1D *hDelayedC = (TH1D*)hDelayed -> Clone();
  hDelayedC -> SetFillColor(kBlue + 1);


  TH1D *hPromptConvolved = new TH1D("hPromptConvolved", "hPromptConvolved; Creation Time (ns); arb. units", 1500, 0, 15000);
  hPromptConvolved -> SetLineColor(kRed);
  hPromptConvolved -> SetLineWidth(2);
  TH1D *hDelayedConvolved = new TH1D("hDelayedConvolved", "hDelayedConvolved", 1500, 0, 15000);
  hDelayedConvolved -> SetLineColor(kBlue + 1);
  hDelayedConvolved -> SetLineWidth(2);
  TH1D *hPOT = new TH1D("hPOT", "hPOT", 1500, 0, 15000);
  hPOT -> SetLineWidth(1);
  
  //Code adapted from MARSlibs quenching to read in POT trace
  int time = 0; 
  char inputstring[256];
  std::ifstream theData("AvgTrace_CsI.txt");

  std::vector<double> *potTrace = new std::vector<double>();
  for (int i = 0; i < 490; i++){
    potTrace -> push_back(0);
  }

  for (int i = 0; i < 1500 - 490; i++){
    potTrace -> push_back(0);
  }
  
  while (theData.getline(inputstring, sizeof(inputstring))){
    if (inputstring[0] == '#'){
      continue; //Don't read comments in the file
    }
    // %lf inside sscanf means 'double'
    if (sscanf(inputstring, "%lf", &(potTrace -> at(time))) != 1){
      break;
    }
    time++;
  }
  theData.close();

  int found = -1;
  int loop = 0;
  while (found == -1){
    if (potTrace -> at(loop) > 0.00001) found = loop;
    loop++;
  }
  std::cout << "Found: " << found << "\n";
  
  for (int i = 0; i < potTrace -> size(); i++){
    if (potTrace -> at(i) > 0){ // If avg charge in bin > 0 -- protons possible
      hPOT -> SetBinContent(i - found, potTrace -> at(i));
    } else{ // If avg charge in bin < 0 -- protons not possible
      hPOT -> SetBinContent(i, 0);
    }
  }
  
  hPOT -> SetLineColor(kBlack);
  // hPOT -> SetLineWidth(2);
  
  // for (int i = 0; i < nuMuTiming -> GetNbinsX(); i++){
  //   hPromptConvolved -> SetBinContent(i, nuMuTiming -> GetBinContent(i) + hPOT -> GetRandom());
  // for (int i = 0; i < hDelayed-> GetNbinsX(); i++){
  //   hDelayedConvolved -> SetBinContent(i, hDelayed -> GetBinContent(i) + hPOT -> GetRandom());

  for (int i = 0; i < nuMuTiming -> GetEntries(); i++){
    hPromptConvolved -> Fill(nuMuTiming -> GetRandom() + hPOT -> GetRandom());
  }
  for (int i = 0; i < hDelayed-> GetEntries(); i++){
    hDelayedConvolved -> Fill(hDelayed -> GetRandom() + hPOT -> GetRandom());
  }
  
  hPromptConvolved -> Scale(1.e3/hPromptConvolved -> Integral());
  hDelayedConvolved -> Scale(1.e3/hDelayedConvolved -> Integral());
  hPOT -> Scale(1.e3/hPOT -> Integral());
  
  TLegend *lEnergy = new TLegend(0.7, 0.6, 0.96, 0.97);
  lEnergy -> SetBorderSize(0);
  lEnergy -> AddEntry(nuMuEnergyC, "#nu_{#mu}", "LE");
  lEnergy -> AddEntry(antiNuMuEnergyC, "#bar{#nu}_{#mu}", "LE");
  lEnergy -> AddEntry(nuEEnergyC, "#nu_{e}", "LE");
  lEnergy -> AddEntry(antiNuEEnergyC, "#bar{#nu}_{e}", "LE");
  // lEnergy -> AddEntry(nuMuEnergyC, "#nu_{#mu}", "F");
  // lEnergy -> AddEntry(antiNuMuEnergyC, "#bar{#nu}_{#mu}", "F");
  // lEnergy -> AddEntry(nuEEnergyC, "#nu_{e}", "F");
  // lEnergy -> AddEntry(antiNuEEnergyC, "#bar{#nu}_{e}", "F");

  TCanvas *cEnergy = new TCanvas("cEnergy", "cEnergy", 1200, 1000);
  gPad -> SetLogy();
  gPad -> SetTopMargin(0.0225);
  gPad -> SetRightMargin(0.03);
   
  nuMuEnergy -> SetXTitle("Energy (MeV)");
  nuMuEnergy -> SetYTitle("arb. units");
  nuMuEnergy -> GetXaxis() -> SetTitleOffset(1.1);
  nuMuEnergy -> GetYaxis() -> SetTitleOffset(1.2);
  nuMuEnergy -> GetXaxis() -> SetTitleSize(0.04);
  nuMuEnergy -> GetYaxis() -> SetTitleSize(0.04);
  nuMuEnergy -> GetXaxis() -> SetLabelSize(0.04);
  nuMuEnergy -> GetYaxis() -> SetLabelSize(0.04);
  nuMuEnergy -> Draw();
  antiNuEEnergy -> Draw("same");
  antiNuMuEnergy -> Draw("same");
  nuEEnergy -> Draw("same");
  lEnergy -> Draw();
  
  cEnergy -> SaveAs("energy.pdf");
  delete cEnergy;

  
  TLegend *lTiming = new TLegend(0.59, 0.65, 0.96, 0.97);
  lTiming -> SetBorderSize(0);
  lTiming -> AddEntry(nuMuTimingC, "Prompt (#nu_{#mu})", "LE");
  lTiming -> AddEntry(hDelayedC, "Delayed (#bar{#nu}_{#mu} + #nu_{e})", "LE");
  lTiming -> AddEntry(hPOT, "Example POT trace", "LE");
  
  TCanvas *cTiming = new TCanvas("cTiming", "cTiming", 1000, 800);
  gPad -> SetLogy();
  gPad -> SetTopMargin(0.0225);
  gPad -> SetRightMargin(0.0225);
   
  hPOT -> Draw();
  hPOT -> SetXTitle("Creation Time (ns since p + Hg)");
  nuMuTiming -> Draw("same");
  hDelayed -> Draw("same");
  lTiming -> Draw();
  
  cTiming -> SaveAs("timing.pdf");
  delete cTiming;


  
  TCanvas *cPE = new TCanvas("cPE", "cPE", 1800, 900);
  gPad -> SetLogy();
  gPad -> SetTopMargin(0.0225);
  gPad -> SetRightMargin(0.0225);
  hPE -> Draw("hist");
  hPE -> GetXaxis() -> SetRangeUser(0, 1050);
  hPE -> GetYaxis() -> SetRangeUser(1e-1, 1e6);
  cPE -> SaveAs("pe.pdf");
  delete cPE;
  
  TCanvas *cPOT = new TCanvas("cPOT", "cPOT", 1200, 1000);
  gPad -> SetLogy();
  gPad -> SetTopMargin(0.0225);
  gPad -> SetRightMargin(0.0225);
  hPOT -> Draw("hist");
  hPOT -> GetYaxis() -> SetRangeUser(1e-10, 0.1);
  cPOT -> SaveAs("pot.pdf");
  delete cPOT;
  
  TCanvas *cConvolved = new TCanvas("cConvolved", "cConvolved", 1200, 1000);
  // gPad -> SetLogy();
  gPad -> SetTopMargin(0.0225);
  gPad -> SetRightMargin(0.0225);
   
  hPOT -> Draw("hist");
  hPOT -> SetXTitle("Creation Time (ns since pulse onset)");
  hPOT -> SetYTitle("arb. units");
  hPOT -> GetXaxis() -> SetTitleOffset(1.1);
  hPOT -> GetYaxis() -> SetTitleOffset(1.2);
  hPOT -> GetXaxis() -> SetTitleSize(0.04);
  hPOT -> GetYaxis() -> SetTitleSize(0.04);
  hPOT -> GetXaxis() -> SetLabelSize(0.04);
  hPOT -> GetYaxis() -> SetLabelSize(0.04);
  hPOT -> GetXaxis() -> SetRangeUser(0, 7500);
  hPOT -> GetYaxis() -> SetRangeUser(0, 27);
  hPromptConvolved -> Draw("hist same");
  hPOT -> Draw("hist same");
  hDelayedConvolved -> Draw("hist same");
  lTiming -> Draw();
  
  cConvolved -> SaveAs("convolved.pdf");
  delete cConvolved;



  TFile *out = new TFile("timingFile.root", "RECREATE");
  nuMuTiming -> Write();
  hDelayed -> Write();
  out -> Close();
  delete out;
  
  return;
}
