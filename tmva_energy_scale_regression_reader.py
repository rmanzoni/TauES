import ROOT
import array

reader = ROOT.TMVA.Reader('Color:Silent')

tau_pt                            = array.array('f',[0]) 
tau_eta                           = array.array('f',[0]) 
tau_mass                          = array.array('f',[0]) 
tau_decayMode                     = array.array('f',[0]) 
 
tau_lead_charged_pt               = array.array('f',[0]) 
tau_lead_neutral_pt               = array.array('f',[0]) 
 
tau_charged_iso                   = array.array('f',[0]) 
tau_gamma_iso                     = array.array('f',[0]) 
tau_neutral_iso                   = array.array('f',[0]) 
tau_charged_sig                   = array.array('f',[0]) 
tau_gamma_sig                     = array.array('f',[0]) 
tau_neutral_sign                  = array.array('f',[0]) 

tau_jet_pt                        = array.array('f',[0]) 
tau_jet_mass                      = array.array('f',[0]) 
tau_jet_nConstituents             = array.array('f',[0]) 
tau_jet_rawFactor                 = array.array('f',[0]) 
tau_jet_chargedHadronEnergy       = array.array('f',[0]) 
tau_jet_neutralHadronEnergy       = array.array('f',[0]) 
tau_jet_neutralEmEnergy           = array.array('f',[0]) 
tau_jet_chargedEmEnergy           = array.array('f',[0]) 
tau_jet_chargedHadronMultiplicity = array.array('f',[0]) 
tau_jet_neutralMultiplicity       = array.array('f',[0]) 

reader.AddVariable( 'tau_pt'                           , tau_pt                           )
reader.AddVariable( 'tau_eta'                          , tau_eta                          )
reader.AddVariable( 'tau_mass'                         , tau_mass                         )
reader.AddVariable( 'tau_decayMode'                    , tau_decayMode                    )
 
reader.AddVariable( 'tau_lead_charged_pt'              , tau_lead_charged_pt              )
reader.AddVariable( 'tau_lead_neutral_pt'              , tau_lead_neutral_pt              )
 
reader.AddVariable( 'tau_charged_iso'                  , tau_charged_iso                  )
reader.AddVariable( 'tau_gamma_iso'                    , tau_gamma_iso                    )
reader.AddVariable( 'tau_neutral_iso'                  , tau_neutral_iso                  )
reader.AddVariable( 'tau_charged_sig'                  , tau_charged_sig                  )
reader.AddVariable( 'tau_gamma_sig'                    , tau_gamma_sig                    )
reader.AddVariable( 'tau_neutral_sign'                 , tau_neutral_sign                 )

reader.AddVariable( 'tau_jet_pt'                       , tau_jet_pt                       )
reader.AddVariable( 'tau_jet_mass'                     , tau_jet_mass                     )
reader.AddVariable( 'tau_jet_nConstituents'            , tau_jet_nConstituents            )
reader.AddVariable( 'tau_jet_rawFactor'                , tau_jet_rawFactor                )
reader.AddVariable( 'tau_jet_chargedHadronEnergy'      , tau_jet_chargedHadronEnergy      )
reader.AddVariable( 'tau_jet_neutralHadronEnergy'      , tau_jet_neutralHadronEnergy      )
reader.AddVariable( 'tau_jet_neutralEmEnergy'          , tau_jet_neutralEmEnergy          )
reader.AddVariable( 'tau_jet_chargedEmEnergy'          , tau_jet_chargedEmEnergy          )
reader.AddVariable( 'tau_jet_chargedHadronMultiplicity', tau_jet_chargedHadronMultiplicity)
reader.AddVariable( 'tau_jet_neutralMultiplicity'      , tau_jet_neutralMultiplicity      )

bdt_label = 'BDTG-7'

# reader.BookMVA('BDT' ,'weights/TMVARegression_BDT-8.weights.xml' )
reader.BookMVA(bdt_label, 'weights/TMVARegression_BDTG-7.weights.xml')
# reader.BookMVA(bdt_label, 'weights/TMVARegression_LD.weights.xml')


f_in = ROOT.TFile.Open('total_tree.root', 'read')
t1 = f_in.Get('tree')


calib   = ROOT.TH1F('calib'  , 'calib'  , 250, 0., 200.) 
uncalib = ROOT.TH1F('uncalib', 'uncalib', 250, 0., 200.) 
gen     = ROOT.TH1F('gen'    , 'gen'    , 250, 0., 200.) 

calib_response   = ROOT.TH1F('calib_response'  , 'calib_response'  , 100, 0., 2.) 
uncalib_response = ROOT.TH1F('uncalib_response', 'uncalib_response', 100, 0., 2.) 


for i, ev in enumerate(t1):
    if i%1000 == 0: 
        print '... processing %d/%d' %(i, t1.GetEntries())
    
    if i >= 200000: break
    if abs(ev.tau_gen_pdgId) != 15: continue

    tau_pt                           [0] = ev.tau_pt                           
    tau_eta                          [0] = ev.tau_eta                          
    tau_mass                         [0] = ev.tau_mass                         
    tau_decayMode                    [0] = ev.tau_decayMode                    
 
    tau_lead_charged_pt              [0] = ev.tau_lead_charged_pt              
    tau_lead_neutral_pt              [0] = ev.tau_lead_neutral_pt              
 
    tau_charged_iso                  [0] = ev.tau_charged_iso                  
    tau_gamma_iso                    [0] = ev.tau_gamma_iso                    
    tau_neutral_iso                  [0] = ev.tau_neutral_iso                  
    tau_charged_sig                  [0] = ev.tau_charged_sig                  
    tau_gamma_sig                    [0] = ev.tau_gamma_sig                    
    tau_neutral_sign                 [0] = ev.tau_neutral_sign                 

    tau_jet_pt                       [0] = ev.tau_jet_pt                       
    tau_jet_mass                     [0] = ev.tau_jet_mass                     
    tau_jet_nConstituents            [0] = ev.tau_jet_nConstituents            
    tau_jet_rawFactor                [0] = ev.tau_jet_rawFactor                
    tau_jet_chargedHadronEnergy      [0] = ev.tau_jet_chargedHadronEnergy      
    tau_jet_neutralHadronEnergy      [0] = ev.tau_jet_neutralHadronEnergy      
    tau_jet_neutralEmEnergy          [0] = ev.tau_jet_neutralEmEnergy          
    tau_jet_chargedEmEnergy          [0] = ev.tau_jet_chargedEmEnergy          
    tau_jet_chargedHadronMultiplicity[0] = ev.tau_jet_chargedHadronMultiplicity
    tau_jet_neutralMultiplicity      [0] = ev.tau_jet_neutralMultiplicity      
         
    calibrated_pt = reader.EvaluateRegression(bdt_label)[0]
    
    calib  .Fill(calibrated_pt)
    uncalib.Fill(ev.tau_pt    )
    gen    .Fill(ev.tau_gen_pt)

    calib_response  .Fill(calibrated_pt/ev.tau_gen_pt)
    uncalib_response.Fill(ev.tau_pt     /ev.tau_gen_pt)


calib  .SetLineColor(ROOT.kRed  )
uncalib.SetLineColor(ROOT.kBlack)
gen    .SetLineColor(ROOT.kGreen)

calib_response  .SetLineColor(ROOT.kRed  )
uncalib_response.SetLineColor(ROOT.kBlack)

uncalib.Draw('HIST'    )
calib  .Draw('HISTSAME')
gen    .Draw('HISTSAME')

ROOT.gPad.SaveAs('plot_%s.pdf' %bdt_label)


uncalib_response.DrawNormalized('HIST')
calib_response.DrawNormalized('HISTSAME')


ROOT.gPad.SaveAs('plot2_%s.pdf' %bdt_label)



outfile = ROOT.TFile.Open('outfile.root', 'recreate')
outfile.cd()
calib_response  .Write()
uncalib_response.Write()
outfile.Close()




