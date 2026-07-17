'use client';
import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import Link from 'next/link';

type BranchEntry = { core: string[], it: string[], gov: string[] };

const BRANCH_DATA: Record<string, BranchEntry> = {
  "computer-science-engineering": {
    core: [
      "Software Engineer", "Software Developer", "Full Stack Developer", "Frontend Developer",
      "Backend Developer", "Web Developer", "Mobile App Developer", "Android Developer",
      "iOS Developer", "Desktop Application Developer"
    ],
    it: [
      "AI Engineer", "Machine Learning Engineer", "Data Scientist", "Data Analyst", "Data Engineer",
      "NLP Engineer", "Computer Vision Engineer", "MLOps Engineer", "Deep Learning Engineer",
      "Prompt Engineer", "LLM Engineer", "Cloud Engineer", "AWS Engineer", "Azure Engineer",
      "Google Cloud Engineer", "DevOps Engineer", "Site Reliability Engineer", "Platform Engineer",
      "Cyber Security Analyst", "Ethical Hacker", "Penetration Tester", "SOC Analyst",
      "Security Engineer", "QA Engineer", "Automation Tester", "Database Administrator",
      "Network Engineer", "Blockchain Developer", "Game Developer", "AR/VR Developer", "Embedded Software Engineer"
    ],
    gov: [
      "NIC Scientist B (National Informatics Centre)", "DRDO Scientist B (IT/Software)",
      "ISRO Scientist/Engineer SC (CS)", "BEL Probationary Engineer (IT)",
      "ECIL Trainee Engineer (CS/IT)", "BSNL JTO (Telecom Software)",
      "Indian Railways IT Officer (RRB)", "SSC CGL (Statistical/Technical Assistant)",
      "UPSC IES – Electronics & Telecom Stream", "State IT Department Officer",
      "GATE Qualified – PSU IT Roles (ONGC, BHEL, GAIL)"
    ]
  },
  "information-technology": {
    core: [
      "Software Engineer", "System Administrator", "Network Engineer", "Cloud Engineer",
      "DevOps Engineer", "IT Support Engineer", "Database Administrator", "Security Analyst"
    ],
    it: [
      "Business Analyst", "Full Stack Developer", "Web Developer", "QA Engineer"
    ],
    gov: [
      "NIC Scientist B", "ECIL Trainee Engineer (IT)", "BEL Probationary Engineer (IT)",
      "DRDO Junior Research Fellow (IT)", "ISRO Scientist SC (IT)", "BSNL JTO",
      "State IT Department Technical Officer", "SSC CGL Technical Assistant",
      "Indian Railways IT Manager (RRB NTPC)", "GATE – PSU IT Recruitment"
    ]
  },
  "artificial-intelligence-and-data-science": {
    core: [
      "AI Engineer", "Machine Learning Engineer", "Deep Learning Engineer", "Data Scientist",
      "Data Analyst", "Data Engineer", "NLP Engineer", "Computer Vision Engineer",
      "Research Engineer", "Prompt Engineer", "LLM Engineer"
    ],
    it: [],
    gov: [
      "DRDO Scientist B (AI/Electronics)", "ISRO Scientist SC (AI/Data)",
      "NIC Scientist B (Data Analytics)", "NITI Aayog Data Fellow",
      "NASSCOM AI Govt Initiatives", "C-DAC Scientist (AI/ML)",
      "CAIR (Centre for AI & Robotics) – DRDO", "IIT/NIT Research Fellowship (GATE)",
      "CSIR Junior Research Fellowship", "DST-Inspire Fellowship"
    ]
  },
  "electronics-and-communication-engineering": {
    core: [
      "Electronics Engineer", "Communication Engineer", "RF Engineer", "Telecom Engineer",
      "PCB Design Engineer", "VLSI Design Engineer", "ASIC Design Engineer", "FPGA Engineer"
    ],
    it: [
      "Embedded Systems Engineer", "Firmware Engineer", "IoT Engineer", "Robotics Engineer",
      "AIoT Engineer", "Network Engineer", "Cyber Security Engineer", "Software Engineer"
    ],
    gov: [
      "DRDO Scientist B (Electronics)", "ISRO Scientist/Engineer SC (ECE)",
      "BEL Probationary Engineer (Electronics)", "ECIL Graduate Engineer Trainee",
      "BSNL JTO (Telecom)", "Indian Army EME Officer", "Indian Navy Engineering Officer",
      "UPSC IES – Electronics & Telecom", "SSC JE (Electrical/Electronics)",
      "TRAI Technical Officer", "HAL Graduate Engineer Trainee", "GATE – BEL, DRDO, ISRO, ECIL"
    ]
  },
  "electrical-and-electronics-engineering": {
    core: [
      "Power Systems Engineer", "Electrical Design Engineer", "Protection Engineer",
      "Substation Engineer", "Transmission Engineer", "Distribution Engineer",
      "Renewable Energy Engineer", "Solar Engineer", "Wind Energy Engineer",
      "PLC Programmer", "SCADA Engineer", "Industrial Automation Engineer",
      "Control Systems Engineer",
    ],
    it: [
      "Embedded Engineer", "Robotics Engineer",
      "IoT Engineer", "AI Engineer", "Data Analyst"
    ],
    gov: [
      "NTPC Executive Trainee (Electrical)", "PGCIL Executive Trainee (Electrical)",
      "BHEL Engineer Trainee (Electrical)", "NPCIL Scientific Officer",
      "State Electricity Board AE/JE", "UPSC IES – Electrical Engineering",
      "SSC JE (Electrical)", "Coal India MT Electrical", "GAIL Executive Trainee",
      "ONGC E1 Engineer (Electrical)", "Indian Railways Electrical Officer (RRB JE/SSE)",
      "GATE – NTPC, PGCIL, BHEL, BPCL"
    ]
  },
  "mechanical-engineering": {
    core: [
      "Design Engineer", "Production Engineer", "Manufacturing Engineer", "Maintenance Engineer",
      "Tool Design Engineer", "Thermal Engineer", "HVAC Engineer", "Quality Engineer",
      "Industrial Engineer", "Plant Engineer"
    ],
    it: [
      "CAD Engineer", "CAM Engineer", "CAE Engineer", "CFD Engineer",
      "Robotics Engineer", "Automation Engineer", "Digital Twin Engineer", "IoT Engineer", "Data Analyst"
    ],
    gov: [
      "BHEL Engineer Trainee (Mechanical)", "DRDO Scientist B (Mechanical)",
      "HAL Graduate Engineer Trainee", "ISRO Scientist SC (Mechanical)",
      "Indian Railways Mechanical Officer (RRB JE/SSE)", "UPSC IES – Mechanical Engineering",
      "SSC JE (Mechanical)", "ONGC E1 Engineer (Mechanical)", "Coal India MT Mechanical",
      "BEL Probationary Engineer (Mechanical)", "SAIL Management Trainee",
      "GATE – BHEL, ONGC, IOCL, HAL, NTPC"
    ]
  },
  "civil-engineering": {
    core: [
      "Site Engineer", "Structural Engineer", "Construction Engineer", "Planning Engineer",
      "Highway Engineer", "Bridge Engineer", "Geotechnical Engineer", "Quantity Surveyor",
      "Water Resources Engineer", "Environmental Engineer"
    ],
    it: [
      "BIM Engineer", "GIS Engineer", "CAD Engineer", "Primavera Planning Engineer"
    ],
    gov: [
      "CPWD Assistant Engineer (Civil)", "PWD Junior Engineer", "State PSC AE/JE (Civil)",
      "UPSC IES – Civil Engineering", "SSC JE (Civil)", "NHAI Assistant Manager",
      "Indian Railways Civil Officer (RRB JE/SSE)", "Municipal Corporation Engineer",
      "WAPCOS Engineer", "RITES Engineer", "NBCC Engineer", "DMRC Civil Engineer",
      "GATE – CPWD, NHAI, DMRC, State PWD"
    ]
  },
  "chemical-engineering": {
    core: [
      "Process Engineer", "Production Engineer", "Plant Engineer", "Safety Engineer",
      "Quality Control Engineer", "Refinery Engineer", "Petrochemical Engineer", "Polymer Engineer"
    ],
    it: [
      "Process Automation Engineer", "Industrial IoT Engineer", "Manufacturing Systems Engineer"
    ],
    gov: [
      "ONGC E1 Engineer (Chemical)", "IOCL Engineer (Chemical)", "BPCL Engineer",
      "HPCL Engineer", "DRDO Scientist B (Chemical)", "BARC Scientific Officer",
      "CSIR Research Associate (Chemical)", "Fertilizer Companies (NFL, GSFC)",
      "UPSC IES – Chemical Engineering (limited)", "GATE – ONGC, IOCL, BPCL, HPCL, GAIL"
    ]
  },
  "automobile-engineering": {
    core: [
      "Automobile Engineer", "Vehicle Design Engineer", "Engine Design Engineer",
      "Vehicle Testing Engineer", "Production Engineer", "Service Engineer"
    ],
    it: [
      "Electric Vehicle Engineer", "ADAS Engineer", "Autonomous Vehicle Engineer", "Automotive Embedded Engineer"
    ],
    gov: [
      "DRDO Scientist B (Automobile/Mech)", "HAL Graduate Engineer Trainee",
      "Indian Army EME Officer", "Ordnance Factory Board (OFB) Engineer",
      "BHEL Engineer Trainee", "State Transport Corporation Engineer",
      "SAIL Management Trainee", "Coal India MT Mechanical",
      "GATE – DRDO, HAL, OFB, BHEL"
    ]
  },
  "biomedical-engineering": {
    core: [
      "Biomedical Engineer", "Medical Device Engineer", "Clinical Engineer",
      "Medical Equipment Engineer", "Rehabilitation Engineer"
    ],
    it: [
      "Health Informatics Engineer", "Bioinformatics Engineer", "Medical Imaging Engineer", "AI Healthcare Engineer"
    ],
    gov: [
      "AIIMS/PGIMER Biomedical Engineer", "DRDO Scientist B (Life Sciences)",
      "ICMR Junior Research Fellow", "DBT Scientist (Biotech/Biomedical)",
      "Government Hospital Biomedical Engineer", "ESIC / CGHS Equipment Engineer",
      "CSIR JRF (Life Sciences)", "DST-Inspire Fellowship",
      "Ministry of Health & Family Welfare Technical Officer"
    ]
  },
  "mechatronics-engineering": {
    core: [
      "Robotics Engineer", "Automation Engineer", "Embedded Engineer",
      "PLC Programmer", "SCADA Engineer", "Control Systems Engineer"
    ],
    it: [
      "Firmware Engineer", "Industrial IoT Engineer"
    ],
    gov: [
      "DRDO Scientist B (Mechatronics)", "ISRO Scientist SC (Mechanical/Electronics)",
      "HAL Graduate Engineer Trainee", "BEL Probationary Engineer",
      "Ordnance Factory Board Engineer", "Indian Army EME Officer",
      "BHEL Engineer Trainee", "GATE – DRDO, HAL, BEL, ISRO"
    ]
  },
  "instrumentation-engineering": {
    core: [
      "Instrumentation Engineer", "Process Control Engineer", "Control Systems Engineer"
    ],
    it: [
      "Automation Engineer", "PLC Engineer", "SCADA Engineer", "Industrial IoT Engineer"
    ],
    gov: [
      "ONGC E1 Engineer (Instrumentation)", "BARC Scientific Officer (Instrumentation)",
      "DRDO Scientist B (Instrumentation)", "BEL Probationary Engineer",
      "ECIL Trainee Engineer (Instrumentation)", "Atomic Minerals Directorate",
      "UPSC IES – Electronics & Telecom", "SSC JE (Electrical/Instrumentation)",
      "GATE – ONGC, BARC, DRDO, BEL, ECIL"
    ]
  },
  "aeronautical-engineering": {
    core: [
      "Aircraft Design Engineer", "Aerodynamics Engineer", "Flight Test Engineer",
      "Propulsion Engineer", "Aircraft Maintenance Engineer"
    ],
    it: [
      "UAV/Drone Engineer", "Aerospace Software Engineer"
    ],
    gov: [
      "ISRO Scientist/Engineer SC (Aerospace)", "DRDO Scientist B (Aeronautical)",
      "HAL Graduate Engineer Trainee (Aeronautical)", "IAF Technical Officer (Engineering)",
      "Indian Navy Aeronautical Engineering Officer", "AAAI Airport Engineer",
      "DGCA Airworthiness Inspector", "NAL (National Aerospace Laboratories)",
      "GATE – ISRO, HAL, DRDO, NAL (Aerospace Engineering)"
    ]
  },
  "agricultural-engineering": {
    core: [
      "Irrigation Engineer", "Farm Machinery Engineer", "Soil & Water Engineer"
    ],
    it: [
      "Precision Agriculture Engineer", "AgriTech Engineer", "Drone Engineer", "Smart Farming Engineer"
    ],
    gov: [
      "ICAR Scientist (Agricultural Engineering)", "State Agriculture Department AE/JE",
      "Water Resources Department Engineer", "NABARD Development Assistant",
      "Central Ground Water Board Scientist", "IARI Research Associate",
      "SSC JE (Irrigation/Agriculture)", "State Irrigation Department Engineer",
      "FAO / UN Agricultural Officer", "GATE – Agricultural Engineering (AG)"
    ]
  },
  "marine-engineering": {
    core: [
      "Marine Engineer", "Ship Design Engineer", "Marine Systems Engineer",
      "Port Engineer", "Offshore Engineer"
    ],
    it: [
      "Marine Automation Engineer"
    ],
    gov: [
      "Merchant Navy Officer (DGMS)", "Indian Navy Marine Engineering Officer",
      "Cochin Shipyard Engineer", "Hindustan Shipyard Limited Engineer",
      "Garden Reach Shipbuilders & Engineers (GRSE)", "Mazagon Dock Shipbuilders",
      "Shipping Corporation of India (SCI) Engineer", "Directorate General of Shipping Officer",
      "ONGC Offshore Engineer", "Port Trust Engineer (Major Ports)"
    ]
  },
  "mining-engineering": {
    core: [
      "Mine Planning Engineer", "Drilling Engineer", "Blasting Engineer",
      "Mineral Processing Engineer", "Mine Safety Engineer", "Exploration Engineer"
    ],
    it: [],
    gov: [
      "Coal India Limited (CIL) MT Mining", "SCCL Mining Engineer",
      "NMDC Mining Engineer", "NLCIL Mining Officer",
      "GSI (Geological Survey of India) Scientist", "IBM (Indian Bureau of Mines) Officer",
      "DGMS Mine Safety Inspector", "MECL Geologist/Drilling Engineer",
      "State Mining Department Engineer", "ONGC Drilling Engineer",
      "UPSC IES – Mining Engineering", "GATE – Mining Engineering (MN)"
    ]
  },
  "industrial-engineering": {
    core: [
      "Industrial Engineer", "Operations Engineer", "Process Improvement Engineer",
      "Supply Chain Engineer", "Logistics Engineer", "Production Planner"
    ],
    it: [],
    gov: [
      "National Productivity Council (NPC) Consultant", "BIS (Bureau of Indian Standards) Officer",
      "DPIIT Industry Officer", "Ministry of Commerce & Industry Officer",
      "NSIC Technical Officer", "State Industries Department Officer",
      "SAIL Management Trainee (Operations)", "BHEL Industrial Engineer",
      "Coal India MT Operations", "GATE – Production & Industrial Engineering (PI)"
    ]
  },
  "production-engineering": {
    core: [
      "Production Engineer", "Manufacturing Engineer", "Quality Engineer",
      "Lean Manufacturing Engineer", "Plant Engineer", "Operations Engineer"
    ],
    it: [],
    gov: [
      "Ordnance Factory Board (OFB) Engineer", "BHEL Engineer Trainee (Production)",
      "HAL Graduate Engineer Trainee", "SAIL Management Trainee",
      "BIS Technical Officer (Quality)", "NSIC Technical Officer",
      "Coal India MT Manufacturing", "DRDO Scientist B (Production)",
      "SSC JE (Mechanical/Production)", "GATE – PI (Production & Industrial)"
    ]
  },
  "metallurgical-engineering": {
    core: [
      "Metallurgical Engineer", "Materials Engineer", "Welding Engineer",
      "Heat Treatment Engineer", "Corrosion Engineer", "Quality Metallurgist"
    ],
    it: [],
    gov: [
      "SAIL Management Trainee (Metallurgy)", "TATA Steel / Govt Steel Plants Metallurgist",
      "RINL (Vizag Steel) Management Trainee", "NMDC Metallurgist",
      "DRDO Scientist B (Materials/Metallurgy)", "BARC Scientific Officer (Metallurgy)",
      "CSIR-NML (National Metallurgical Laboratory) Scientist",
      "UPSC IES – Metallurgical Engineering", "GATE – Metallurgical Engineering (MT)"
    ]
  },
  "petroleum-engineering": {
    core: [
      "Drilling Engineer", "Reservoir Engineer", "Production Engineer",
      "Completion Engineer", "Well Testing Engineer", "Offshore Engineer"
    ],
    it: [],
    gov: [
      "ONGC E1 Engineer (Petroleum/Drilling)", "OIL India Limited Engineer",
      "BPCL Engineer (Petroleum)", "HPCL Engineer",
      "MRPL Engineer", "IOCL Engineer (Petroleum)",
      "Directorate General of Hydrocarbons (DGH) Officer",
      "GAIL Engineer (Gas/Petroleum)", "EIL Engineer (Petroleum)",
      "GATE – Petroleum Engineering (PE)"
    ]
  },
  "textile-engineering": {
    core: [
      "Textile Engineer", "Fabric Production Engineer", "Garment Production Engineer",
      "Textile Quality Engineer", "Textile Design Engineer"
    ],
    it: [],
    gov: [
      "NITRA (National Institute of Technical Research on Advancing Textiles) Scientist",
      "Textile Commissioner's Office Technical Officer",
      "MSME Technology Centre (Weaving) Officer",
      "ATIRA / BTRA / SITRA Research Associate",
      "State Handloom & Textile Department Officer",
      "NHDC (National Handloom Development Corporation) Officer",
      "Ministry of Textiles Technical Expert",
      "BIS Technical Officer (Textiles)", "Export Promotion Councils (AEPC, TEXPROCIL)"
    ]
  },
  "biotechnology-engineering": {
    core: [
      "Biotechnologist", "Pharmaceutical Research Associate",
      "Clinical Research Associate", "Biomedical Research Scientist"
    ],
    it: [
      "Bioinformatics Engineer", "Genetic Engineer"
    ],
    gov: [
      "DBT (Dept of Biotechnology) Scientist", "CSIR Junior Research Fellow (Life Sci)",
      "ICMR Scientist B", "ICAR Scientist (Agri Biotech)",
      "DRDO Scientist B (Life Sciences)", "BIRAC (Biotech Industry Research Assistance Council)",
      "DST-Inspire Faculty Fellowship", "IISC/IIT Research Associate",
      "Ministry of Health Technical Officer (Biotech)",
      "GATE – Biotechnology (BT) – IIT/IISc M.Tech + PSU"
    ]
  },
  "food-technology": {
    core: [
      "Food Process Engineer", "Food Safety Officer", "Quality Assurance Engineer",
      "Product Development Engineer", "Packaging Engineer"
    ],
    it: [],
    gov: [
      "FSSAI Food Safety Officer", "DFPD (Food & Public Distribution) Officer",
      "ICAR-CIFRI / CFTRI Scientist (Food Technology)", "CSIR-CFTRI Research Associate",
      "State Food Safety Officer (FSSAI Empanelled)", "Agmark Quality Officer",
      "Ministry of Food Processing Industries Officer", "DRDO Scientist (Food & Nutrition)",
      "NAFED / FCI Food Inspector", "NHB (National Horticulture Board) Officer"
    ]
  },
  "environmental-engineering": {
    core: [
      "Environmental Engineer", "Waste Management Engineer", "Water Treatment Engineer",
      "Air Pollution Control Engineer", "Sustainability Consultant", "Environmental Compliance Engineer"
    ],
    it: [],
    gov: [
      "CPCB (Central Pollution Control Board) Scientist", "State PCB (Pollution Control Board) Officer",
      "MoEFCC (Ministry of Environment) Technical Officer",
      "National Water Mission Officer", "NEERI Scientist (CSIR)",
      "Forest Survey of India Officer", "TERI Research Associate",
      "National Clean Air Programme (NCAP) Officer", "UPSC IES – Environmental Engineering",
      "SSC JE (Environmental/Civil)", "NMCG (National Mission for Clean Ganga) Engineer",
      "GATE – Environmental Engineering (Civil branch + ES paper)"
    ]
  }
};

type TabType = "core" | "it" | "gov";

const GOV_EXAMS = [
  { name: "GATE", desc: "Graduate Aptitude Test in Engineering – PSU recruitment & M.Tech/PhD admissions." },
  { name: "UPSC IES/ESE", desc: "Engineering Services Examination – Central Govt Engineering posts." },
  { name: "SSC JE", desc: "Staff Selection Commission Junior Engineer – Central Govt projects." },
  { name: "State PSC AE/JE", desc: "Assistant Engineer & Junior Engineer exams by State Public Service Commissions." },
  { name: "DRDO SET", desc: "DRDO Scientist Entry Test – Defence Research & Development Organisation." },
  { name: "ISRO Centralised Recruitment", desc: "Scientist/Engineer SC – Indian Space Research Organisation." },
];

export default function BranchCareerExplorer({ params }: { params: { branch: string } }) {
  const branchKey = params.branch;
  const branchName = decodeURIComponent(branchKey).replace(/-/g, ' ').replace(/\b\w/g, l => l.toUpperCase());
  const branchData = BRANCH_DATA[branchKey] || { core: ["Engineer"], it: ["Software Engineer"], gov: [] };
  const [activeTab, setActiveTab] = useState<TabType>("core");

  const toSlug = (career: string) => career.toLowerCase().replace(/ \/ | & |\/| & /g, '-').replace(/\s+/g, '-').replace(/[^a-z0-9-]/g, '');

  const TABS = [
    { key: "core" as TabType, label: "🏗️ Core Careers", color: "blue", activeClass: "bg-blue-600 text-white shadow-lg", borderClass: "border-blue-500/20 bg-blue-500/5 hover:bg-blue-500/10", textClass: "group-hover:text-blue-500", linkClass: "text-blue-500", desc: "Master the core engineering skills for this role." },
    { key: "it" as TabType, label: "💻 IT & Digital Careers", color: "purple", activeClass: "bg-purple-600 text-white shadow-lg", borderClass: "border-purple-500/20 bg-purple-500/5 hover:bg-purple-500/10", textClass: "group-hover:text-purple-500", linkClass: "text-purple-500", desc: "Transition into this high-demand tech role." },
    { key: "gov" as TabType, label: "🏛️ Government & PSU", color: "pink", activeClass: "bg-pink-600 text-white shadow-lg", borderClass: "border-pink-500/20 bg-pink-500/5 hover:bg-pink-500/10", textClass: "group-hover:text-pink-500", linkClass: "text-pink-500", desc: "Secure a prestigious government or PSU position." },
  ];

  const activeTabConfig = TABS.find(t => t.key === activeTab)!;
  const currentCareers = branchData[activeTab] || [];

  return (
    <main className="flex min-h-screen flex-col items-center pt-24 pb-16 px-6 max-w-7xl mx-auto">
      <div className="w-full mb-8">
        <Link href="/dashboard" className="text-blue-500 hover:underline mb-4 inline-block">← Back to Dashboard</Link>
        <h1 className="text-4xl md:text-5xl font-bold mb-3">
          Careers for <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-500 to-purple-600">{branchName}</span>
        </h1>
        <p className="text-foreground/70 text-lg">Explore Core, IT & Digital, and Government/PSU opportunities for your branch.</p>
      </div>

      {/* Tab Bar */}
      <div className="w-full flex gap-3 mb-8 border-b border-foreground/10 pb-4 overflow-x-auto">
        {TABS.map(tab => (
          <button
            key={tab.key}
            onClick={() => setActiveTab(tab.key)}
            className={`px-6 py-3 font-semibold rounded-lg whitespace-nowrap transition-all ${activeTab === tab.key ? tab.activeClass : 'bg-foreground/5 hover:bg-foreground/10'}`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Career Count Badge */}
      {activeTab !== "gov" && (
        <div className="w-full mb-6">
          <span className="px-4 py-1.5 rounded-full text-sm font-semibold bg-foreground/10 text-foreground/70">
            {currentCareers.length} Career{currentCareers.length !== 1 ? 's' : ''} Available
          </span>
        </div>
      )}

      <div className="w-full min-h-[50vh]">
        <AnimatePresence mode="wait">

          {/* Core & IT Tab Content */}
          {(activeTab === "core" || activeTab === "it") && (
            <motion.div
              key={activeTab}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
            >
              {currentCareers.length > 0 ? currentCareers.map((career) => (
                <Link href={`/careers/${toSlug(career)}`} key={career}>
                  <div className={`p-6 rounded-xl border ${activeTabConfig.borderClass} transition-colors h-full flex flex-col justify-between shadow-sm group cursor-pointer`}>
                    <div>
                      <h3 className={`text-xl font-bold mb-2 ${activeTabConfig.textClass} transition-colors`}>{career}</h3>
                      <p className="text-sm text-foreground/70">{activeTabConfig.desc}</p>
                    </div>
                    <div className={`mt-4 ${activeTabConfig.linkClass} font-medium text-sm flex items-center gap-1`}>
                      Open Roadmap <span>→</span>
                    </div>
                  </div>
                </Link>
              )) : (
                <div className="col-span-full text-center py-16 text-foreground/50">
                  <p className="text-5xl mb-4">🔍</p>
                  <p className="text-lg font-semibold">No specific careers listed for this tab.</p>
                  <p>Check the Core Careers tab or browse other branches.</p>
                </div>
              )}
            </motion.div>
          )}

          {/* Government & PSU Tab Content */}
          {activeTab === "gov" && (
            <motion.div
              key="gov"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              className="w-full space-y-8"
            >
              {/* PSU Roles */}
              <div>
                <h2 className="text-2xl font-bold mb-4 text-pink-600 dark:text-pink-400">
                  🏛️ Government & PSU Roles for {branchName}
                </h2>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {branchData.gov.length > 0 ? branchData.gov.map((role) => (
                    <div key={role} className="p-5 rounded-xl border border-pink-500/20 bg-pink-500/5 hover:bg-pink-500/10 transition-colors group">
                      <div className="flex items-start gap-3">
                        <span className="text-2xl">🏅</span>
                        <div>
                          <p className="font-semibold group-hover:text-pink-500 transition-colors">{role}</p>
                        </div>
                      </div>
                    </div>
                  )) : (
                    <p className="text-foreground/50 col-span-full">No specific PSU roles listed yet for this branch.</p>
                  )}
                </div>
              </div>

              {/* Competitive Exams */}
              <div className="bg-foreground/5 rounded-2xl border border-foreground/10 p-8">
                <h3 className="text-xl font-bold mb-6">📝 Key Competitive Exams</h3>
                <div className="grid md:grid-cols-2 gap-4">
                  {GOV_EXAMS.map(exam => (
                    <div key={exam.name} className="flex gap-3 p-4 bg-background rounded-xl border border-foreground/10">
                      <span className="font-bold text-pink-500 min-w-fit">{exam.name}</span>
                      <span className="text-sm text-foreground/70">{exam.desc}</span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Top PSU Companies */}
              <div className="bg-foreground/5 rounded-2xl border border-foreground/10 p-8">
                <h3 className="text-xl font-bold mb-4">🏢 Top Recruiting PSUs & Govt Organizations</h3>
                <div className="flex flex-wrap gap-3">
                  {["BHEL", "BEL", "DRDO", "ISRO", "ONGC", "NTPC", "PGCIL", "IOCL", "BPCL", "HPCL", "GAIL", "SAIL", "Coal India", "HAL", "ECIL", "BARC", "NPCIL", "Indian Railways", "DMRC", "CPWD", "NHPC", "NALCO", "RINL", "OIL India"].map(org => (
                    <span key={org} className="px-3 py-1.5 bg-pink-500/10 text-pink-700 dark:text-pink-300 border border-pink-500/20 rounded-full text-sm font-semibold">{org}</span>
                  ))}
                </div>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </main>
  );
}
