# app.py
# Streamlit Anatomy MCQ Trainer with PDF summary
#
# How to run:
#   pip install streamlit fpdf
#   streamlit run app.py



import streamlit as st
from io import StringIO
import random
from datetime import datetime

# -----------------------------
# 1. QUESTION BANK
# -----------------------------
# You can extend this list with as many questions as you want.
# Each question is a dict with:
#  - id: unique int
#  - topic: string (used for filtering)
#  - question: string
#  - options: list of 4 strings
#  - answer_index: int (0-3)
#  - explanation: string

QUESTION_BANK = [
    # --- Anatomical Terms & Planes ---
    {
        "id": 1,
        "topic": "Anatomical Terms & Planes",
        "question": "In the standard anatomical position, which statement is TRUE?",
        "options": [
            "The palms face forwards with the thumbs lateral",
            "The palms face backwards with the thumbs medial",
            "The body lies supine with the face upwards",
            "The arms are abducted to 90 degrees from the trunk"
        ],
        "answer_index": 0,
        "explanation": (
            "In the anatomical position the person stands upright, looks forwards, "
            "upper limbs by the sides, feet close together, and palms facing forwards. "
            "The thumb is lateral in this position."
        ),
    },
    {
        "id": 2,
        "topic": "Anatomical Terms & Planes",
        "question": "A plane that divides the body into unequal right and left parts is called:",
        "options": [
            "Sagittal plane",
            "Median (midsagittal) plane",
            "Coronal plane",
            "Transverse plane"
        ],
        "answer_index": 0,
        "explanation": (
            "The median plane divides the body into EQUAL right and left halves. "
            "Any plane parallel to it but not in the midline is a sagittal plane. "
            "Coronal planes divide into anterior/posterior and transverse into superior/inferior."
        ),
    },
    {
        "id": 3,
        "topic": "Anatomical Terms & Planes",
        "question": "Which of the following pairs is CORRECTLY matched?",
        "options": [
            "Proximal – nearer to the trunk or origin",
            "Distal – nearer to the median plane",
            "Superficial – away from the surface of the body",
            "Central – away from the brain and spinal cord"
        ],
        "answer_index": 0,
        "explanation": (
            "Proximal means nearer to the trunk or to the point of origin, "
            "distal means further away. Superficial is closer to the surface, "
            "deep is away from the surface. Central is towards the brain/spinal cord."
        ),
    },

    # --- Membrane Transport ---
    {
        "id": 10,
        "topic": "Membrane Transport",
        "question": "Simple diffusion across a cell membrane:",
        "options": [
            "Does not require energy and is not saturable",
            "Requires ATP and is saturable",
            "Requires carrier proteins and is saturable",
            "Moves solute against its concentration gradient"
        ],
        "answer_index": 0,
        "explanation": (
            "In simple diffusion, molecules move down their concentration gradient "
            "directly through the lipid bilayer or through channels. No energy is required "
            "and the rate is not saturable because no carriers are involved."
        ),
    },
    {
        "id": 11,
        "topic": "Membrane Transport",
        "question": "Facilitated diffusion differs from simple diffusion because:",
        "options": [
            "It can show saturation due to limited carriers",
            "It moves solutes against their gradient",
            "It always requires ATP hydrolysis",
            "It only transports water molecules"
        ],
        "answer_index": 0,
        "explanation": (
            "Facilitated diffusion still moves molecules down their electrochemical gradient, "
            "so it does not require ATP. However, it uses specific carrier proteins, so the process "
            "can saturate when all carriers are occupied, showing a T_max."
        ),
    },
    {
        "id": 12,
        "topic": "Membrane Transport",
        "question": "The Na⁺/K⁺-ATPase pump:",
        "options": [
            "Pumps 3 Na⁺ out and 2 K⁺ in using ATP",
            "Pumps 2 Na⁺ in and 3 K⁺ out using ATP",
            "Is an example of secondary active transport",
            "Moves ions down their concentration gradients"
        ],
        "answer_index": 0,
        "explanation": (
            "The Na⁺/K⁺-ATPase is a primary active transporter. For each ATP hydrolysed "
            "it pumps 3 Na⁺ ions out of the cell and 2 K⁺ ions into the cell, both against "
            "their concentration gradients."
        ),
    },

    # --- Epithelium & Glands ---
    {
        "id": 20,
        "topic": "Epithelium & Glands",
        "question": "Simple squamous epithelium is BEST suited for which function?",
        "options": [
            "Rapid diffusion across thin barriers",
            "Protection from mechanical abrasion",
            "Secretion of thick mucus",
            "Stretching to accommodate distension"
        ],
        "answer_index": 0,
        "explanation": (
            "Simple squamous epithelium is very thin and allows rapid diffusion and filtration. "
            "It lines structures like alveoli, endothelium of blood vessels, and Bowman's capsule."
        ),
    },
    {
        "id": 21,
        "topic": "Epithelium & Glands",
        "question": "Stratified squamous non-keratinised epithelium is typically found in:",
        "options": [
            "Oesophagus and vagina",
            "Skin (epidermis)",
            "Alveoli of lungs",
            "Urinary bladder"
        ],
        "answer_index": 0,
        "explanation": (
            "Stratified squamous non-keratinised epithelium lines moist surfaces exposed to abrasion "
            "but kept moist, such as the oral cavity, oesophagus, and vagina. The skin has keratinised "
            "stratified squamous epithelium. The bladder has transitional epithelium."
        ),
    },
    {
        "id": 22,
        "topic": "Epithelium & Glands",
        "question": "An exocrine gland that releases its secretion via exocytosis without loss of cytoplasm is:",
        "options": [
            "Merocrine gland",
            "Apocrine gland",
            "Holocrine gland",
            "Endocrine gland"
        ],
        "answer_index": 0,
        "explanation": (
            "Merocrine glands (e.g. most sweat glands, salivary glands) secrete by exocytosis only. "
            "Apocrine glands lose part of their apical cytoplasm, and holocrine glands release whole cells "
            "that disintegrate (e.g. sebaceous glands). Endocrine glands are ductless and secrete into blood."
        ),
    },

    # --- Connective Tissue, Cartilage & Bone ---
    {
        "id": 30,
        "topic": "Connective Tissue, Cartilage & Bone",
        "question": "The principal fibre type providing tensile strength to connective tissue is:",
        "options": [
            "Collagen fibres",
            "Elastic fibres",
            "Reticular fibres",
            "Actin filaments"
        ],
        "answer_index": 0,
        "explanation": (
            "Collagen fibres (especially type I) are thick, strong fibres that resist stretching "
            "and provide tensile strength to connective tissues such as tendons and ligaments."
        ),
    },
    {
        "id": 31,
        "topic": "Connective Tissue, Cartilage & Bone",
        "question": "Hyaline cartilage is typically found in all of the following EXCEPT:",
        "options": [
            "Articular surfaces of synovial joints",
            "Costal cartilages",
            "Epiphyseal growth plates",
            "Intervertebral discs"
        ],
        "answer_index": 3,
        "explanation": (
            "Intervertebral discs are mainly fibrocartilage, which has abundant type I collagen in bundles. "
            "Hyaline cartilage is found in articular cartilage, costal cartilages, respiratory tract cartilages, "
            "and growth plates."
        ),
    },
    {
        "id": 32,
        "topic": "Connective Tissue, Cartilage & Bone",
        "question": "Compact bone is organised into structural units called:",
        "options": [
            "Osteons (Haversian systems)",
            "Lobules",
            "Sarcoplasmic units",
            "Acini"
        ],
        "answer_index": 0,
        "explanation": (
            "Compact bone is arranged into cylindrical units called osteons or Haversian systems, "
            "each with a central Haversian canal surrounded by concentric lamellae of bone matrix."
        ),
    },

    # --- Joints & Muscle ---
    {
        "id": 40,
        "topic": "Joints & Muscle",
        "question": "A freely movable joint with a joint cavity, articular cartilage, and synovial membrane is a:",
        "options": [
            "Synovial joint",
            "Fibrous joint",
            "Primary cartilaginous joint",
            "Secondary cartilaginous joint"
        ],
        "answer_index": 0,
        "explanation": (
            "Synovial joints are diarthroses and have a joint cavity, articular (hyaline) cartilage, "
            "a fibrous capsule, and a synovial membrane. Fibrous and cartilaginous joints lack a synovial cavity "
            "and are usually less mobile."
        ),
    },
    {
        "id": 41,
        "topic": "Joints & Muscle",
        "question": "Which pair of movement and joint type is MOST appropriate?",
        "options": [
            "Hinge joint – flexion and extension",
            "Pivot joint – circumduction",
            "Ball-and-socket joint – only flexion/extension",
            "Saddle joint – no axial rotation or movement"
        ],
        "answer_index": 0,
        "explanation": (
            "Hinge joints (e.g. elbow) mainly allow flexion and extension. Pivot joints allow rotation "
            "around one axis (e.g. atlanto-axial). Ball-and-socket joints allow multiaxial movement. "
            "Saddle joints allow biaxial movement (e.g. thumb carpometacarpal joint)."
        ),
    },
    {
        "id": 42,
        "topic": "Joints & Muscle",
        "question": "The basic functional (contractile) unit of a skeletal muscle fibre is the:",
        "options": [
            "Sarcomere",
            "Myofibril",
            "Muscle fascicle",
            "Motor unit"
        ],
        "answer_index": 0,
        "explanation": (
            "Sarcomeres are the repeating units between two Z lines within a myofibril. "
            "They contain the thick and thin filaments whose interaction produces muscle contraction."
        ),
    },

    # --- Nervous Tissue & CNS/ANS ---
    {
        "id": 50,
        "topic": "Nervous System (CNS & PNS)",
        "question": "Which statement about myelination is TRUE?",
        "options": [
            "Oligodendrocytes myelinate axons in the CNS",
            "Schwann cells myelinate axons in the CNS",
            "Oligodendrocytes myelinate only one internode on a single axon",
            "Unmyelinated axons cannot conduct impulses"
        ],
        "answer_index": 0,
        "explanation": (
            "In the CNS, myelination is by oligodendrocytes, each of which can myelinate parts of several axons. "
            "In the PNS, Schwann cells myelinate one segment of one axon. Unmyelinated axons still conduct, "
            "but more slowly and continuously."
        ),
    },
    {
        "id": 51,
        "topic": "Nervous System (CNS & PNS)",
        "question": "The dorsal root of a spinal nerve contains:",
        "options": [
            "Sensory (afferent) fibres",
            "Motor (efferent) fibres only",
            "Mixed sensory and motor fibres",
            "Autonomic fibres only"
        ],
        "answer_index": 0,
        "explanation": (
            "The dorsal (posterior) root carries sensory afferent fibres from the periphery to the spinal cord "
            "and contains the dorsal root ganglion. The ventral (anterior) root carries motor efferent fibres. "
            "They join to form a mixed spinal nerve."
        ),
    },
    {
        "id": 52,
        "topic": "ANS",
        "question": "The sympathetic division of the autonomic nervous system has its preganglionic neurons in:",
        "options": [
            "Thoracolumbar segments of the spinal cord",
            "Craniosacral segments of the CNS",
            "Only cervical spinal cord segments",
            "Only sacral spinal cord segments"
        ],
        "answer_index": 0,
        "explanation": (
            "Sympathetic outflow is thoracolumbar, from the intermediolateral cell columns of T1–L2 segments. "
            "Parasympathetic outflow is craniosacral (brainstem nuclei of cranial nerves III, VII, IX, X and S2–S4)."
        ),
    },
    {
        "id": 53,
        "topic": "ANS",
        "question": "Which of the following is typically a parasympathetic effect?",
        "options": [
            "Constriction of the pupil",
            "Increased heart rate and contractility",
            "Bronchodilation",
            "Reduced gastrointestinal motility"
        ],
        "answer_index": 0,
        "explanation": (
            "Parasympathetic stimulation generally promotes 'rest and digest' functions: "
            "pupillary constriction, increased GI motility and secretions, and reduced heart rate."
        ),
    },

    # --- Heart & Blood Vessels ---
    {
        "id": 60,
        "topic": "Heart & Blood Vessels",
        "question": "The apex of the heart is formed mainly by the:",
        "options": [
            "Left ventricle",
            "Right ventricle",
            "Left atrium",
            "Right atrium"
        ],
        "answer_index": 0,
        "explanation": (
            "The apex of the heart lies in the left 5th intercostal space in the mid-clavicular line "
            "and is formed mainly by the left ventricle."
        ),
    },
    {
        "id": 61,
        "topic": "Heart & Blood Vessels",
        "question": "Which valve prevents backflow of blood from the right ventricle to the right atrium?",
        "options": [
            "Tricuspid valve",
            "Pulmonary valve",
            "Mitral (bicuspid) valve",
            "Aortic valve"
        ],
        "answer_index": 0,
        "explanation": (
            "The tricuspid valve is the right atrioventricular valve, guarding the orifice between "
            "the right atrium and right ventricle."
        ),
    },
    {
        "id": 62,
        "topic": "Heart & Blood Vessels",
        "question": "Elastic arteries, such as the aorta, are characterised by:",
        "options": [
            "Abundant elastic lamellae in the tunica media",
            "A very thick tunica adventitia only",
            "Absence of endothelium",
            "Having valves similar to veins"
        ],
        "answer_index": 0,
        "explanation": (
            "Elastic arteries have many concentric elastic lamellae in the tunica media, "
            "allowing them to stretch during systole and recoil during diastole. "
            "They still have an endothelium and do not possess valves."
        ),
    },

    # --- Lymphatic System ---
    {
        "id": 70,
        "topic": "Lymphatic System",
        "question": "The main function of lymph nodes is to:",
        "options": [
            "Filter lymph and initiate immune responses",
            "Produce erythrocytes",
            "Store bile",
            "Produce surfactant"
        ],
        "answer_index": 0,
        "explanation": (
            "Lymph nodes filter lymph through a network of sinuses and contain lymphocytes and macrophages "
            "that can initiate immune responses against antigens carried in the lymph."
        ),
    },
    {
        "id": 71,
        "topic": "Lymphatic System",
        "question": "Which lymphoid organ is the main site of T-lymphocyte maturation?",
        "options": [
            "Thymus",
            "Spleen",
            "Lymph node",
            "Tonsil"
        ],
        "answer_index": 0,
        "explanation": (
            "The thymus is a primary lymphoid organ where T cells mature. "
            "The spleen, lymph nodes, and tonsils are secondary lymphoid organs where immune responses occur."
        ),
    },

    # --- Respiratory System ---
    {
        "id": 80,
        "topic": "Respiratory System",
        "question": "The functional unit of gas exchange in the lung is the:",
        "options": [
            "Alveolus",
            "Terminal bronchiole",
            "Segmental bronchus",
            "Main bronchus"
        ],
        "answer_index": 0,
        "explanation": (
            "Gas exchange occurs across the thin walls of the alveoli and their associated capillaries, "
            "forming the blood–air barrier."
        ),
    },
    {
        "id": 81,
        "topic": "Respiratory System",
        "question": "Which statement about the right lung is CORRECT?",
        "options": [
            "It has three lobes separated by two fissures",
            "It is smaller than the left lung because of the heart",
            "It has only an oblique fissure",
            "It has a cardiac notch on its medial surface"
        ],
        "answer_index": 0,
        "explanation": (
            "The right lung is larger and has three lobes (upper, middle, lower) separated by an oblique and a horizontal fissure. "
            "The left lung has two lobes and a cardiac notch."
        ),
    },

    # --- Urinary System ---
    {
        "id": 90,
        "topic": "Urinary System",
        "question": "The functional unit of the kidney where filtration of blood occurs is the:",
        "options": [
            "Nephron",
            "Collecting duct",
            "Renal pelvis",
            "Ureter"
        ],
        "answer_index": 0,
        "explanation": (
            "Each nephron begins with a renal corpuscle (glomerulus + Bowman's capsule) where filtration occurs. "
            "The filtrate then passes through the tubules and collecting system."
        ),
    },
    {
        "id": 91,
        "topic": "Urinary System",
        "question": "Which structure directly carries urine from the kidney to the urinary bladder?",
        "options": [
            "Ureter",
            "Urethra",
            "Renal artery",
            "Renal vein"
        ],
        "answer_index": 0,
        "explanation": (
            "The ureters are muscular tubes that convey urine from the renal pelvis of each kidney to the urinary bladder."
        ),
    },

    # --- Endocrine Intro ---
    {
        "id": 100,
        "topic": "Endocrine System",
        "question": "Which of the following is a purely endocrine gland (no exocrine function)?",
        "options": [
            "Pituitary gland",
            "Pancreas",
            "Testis",
            "Ovary"
        ],
        "answer_index": 0,
        "explanation": (
            "The anterior and posterior pituitary are purely endocrine. "
            "The pancreas, ovaries, and testes have both endocrine and exocrine components."
        ),
    },
    {
        "id": 101,
        "topic": "Endocrine System",
        "question": "Endocrine hormones typically reach their target organs by:",
        "options": [
            "Travelling in the bloodstream",
            "Passing through ducts to body surfaces",
            "Moving between cells via desmosomes",
            "Being stored in synaptic vesicles at neuromuscular junctions"
        ],
        "answer_index": 0,
        "explanation": (
            "Endocrine glands are ductless and secrete hormones into the interstitial fluid, "
            "from where they enter the bloodstream and travel to distant target organs."
        ),
    },

    # --- Male Reproductive ---
    {
        "id": 110,
        "topic": "Male Reproductive System",
        "question": "The primary site of sperm production in the testis is the:",
        "options": [
            "Seminiferous tubules",
            "Epididymis",
            "Vas deferens",
            "Rete testis"
        ],
        "answer_index": 0,
        "explanation": (
            "Spermatogenesis occurs in the seminiferous tubules of the testis. "
            "The epididymis stores and matures sperm; the vas deferens transports them."
        ),
    },
    {
        "id": 111,
        "topic": "Male Reproductive System",
        "question": "Which cells in the testis form the blood–testis barrier and support developing sperm cells?",
        "options": [
            "Sertoli cells",
            "Leydig cells",
            "Spermatogonia",
            "Macrophages"
        ],
        "answer_index": 0,
        "explanation": (
            "Sertoli cells are tall supporting cells in the seminiferous tubules. "
            "They form tight junctions (blood–testis barrier), nourish developing germ cells, "
            "and secrete factors needed for spermatogenesis. Leydig cells secrete testosterone."
        ),
    },

    # --- Female Reproductive ---
    {
        "id": 120,
        "topic": "Female Reproductive System",
        "question": "The usual site of fertilisation of the ovum is the:",
        "options": [
            "Ampulla of the uterine tube",
            "Infundibulum of the uterine tube",
            "Cervical canal",
            "Vaginal fornix"
        ],
        "answer_index": 0,
        "explanation": (
            "Fertilisation most commonly occurs in the ampulla, the widest part of the uterine (Fallopian) tube."
        ),
    },
    {
        "id": 121,
        "topic": "Female Reproductive System",
        "question": "A normal uterus is described as:",
        "options": [
            "Anteverted and anteflexed",
            "Retroverted and retroflexed",
            "Fully vertical with no angulation",
            "Inverted into the vaginal canal"
        ],
        "answer_index": 0,
        "explanation": (
            "In most women the uterus is anteverted (tilted forwards relative to the vagina) and anteflexed "
            "(body bent forwards relative to the cervix). Retroversion/retroflexion can predispose to prolapse."
        ),
    },

    # --- Cell Division & Early Embryology (very basic, can be expanded) ---
    {
        "id": 130,
        "topic": "Cell Division & Early Embryology",
        "question": "Meiosis differs from mitosis mainly because meiosis:",
        "options": [
            "Produces haploid gametes with half the chromosome number",
            "Occurs in all somatic cells",
            "Produces genetically identical daughter cells",
            "Has only one cell division"
        ],
        "answer_index": 0,
        "explanation": (
            "Meiosis occurs in germ cells and involves two cell divisions, producing haploid gametes "
            "that are genetically diverse. Mitosis produces diploid daughter cells identical to the parent cell."
        ),
    },
    {
        "id": 131,
        "topic": "Cell Division & Early Embryology",
        "question": "The morula is best described as:",
        "options": [
            "A solid ball of blastomeres formed by cleavage divisions",
            "A hollow sphere with an inner cell mass and trophoblast",
            "The stage after implantation into the endometrium",
            "The bilaminar embryonic disc"
        ],
        "answer_index": 0,
        "explanation": (
            "The morula is a solid ball of blastomeres formed around day 3–4 after fertilisation. "
            "Fluid then accumulates to form the blastocyst with inner cell mass and trophoblast."
        ),
    },
]

NEW_QUESTIONS = [
    # =========================
    # Anatomical Terms & Planes
    # =========================
    {
        "id": 200,
        "topic": "Anatomical Terms & Planes",
        "question": "Which term best describes a structure located closer to the midline of the body?",
        "options": [
            "Medial",
            "Lateral",
            "Superficial",
            "Distal"
        ],
        "answer_index": 0,
        "explanation": (
            "Medial means nearer to the median plane. Lateral means further away from it. "
            "Superficial and distal describe other relationships (depth and distance from origin)."
        ),
    },
    {
        "id": 201,
        "topic": "Anatomical Terms & Planes",
        "question": "The coronal (frontal) plane divides the body into:",
        "options": [
            "Anterior and posterior parts",
            "Right and left halves only",
            "Superior and inferior parts",
            "Proximal and distal parts"
        ],
        "answer_index": 0,
        "explanation": (
            "Coronal (frontal) planes divide the body into anterior (front) and posterior (back) portions. "
            "Median and sagittal planes divide into right and left, and transverse planes into superior and inferior."
        ),
    },
    {
        "id": 202,
        "topic": "Anatomical Terms & Planes",
        "question": "Which of the following movements occurs mainly in the transverse plane?",
        "options": [
            "Medial rotation of the shoulder",
            "Flexion at the elbow",
            "Abduction at the hip",
            "Plantarflexion at the ankle"
        ],
        "answer_index": 0,
        "explanation": (
            "Rotational movements (medial and lateral rotation) mainly occur in the transverse plane around a vertical axis. "
            "Flexion/extension usually occur in the sagittal plane; abduction/adduction in the coronal plane."
        ),
    },
    {
        "id": 203,
        "topic": "Anatomical Terms & Planes",
        "question": "Which term correctly describes the position of the skin relative to skeletal muscles?",
        "options": [
            "Superficial",
            "Deep",
            "Proximal",
            "Distal"
        ],
        "answer_index": 0,
        "explanation": (
            "The skin is superficial (closer to the body surface) compared with skeletal muscles, which are deeper. "
            "Proximal and distal refer to distance from the trunk or origin, not depth."
        ),
    },
    {
        "id": 204,
        "topic": "Anatomical Terms & Planes",
        "question": "A structure found on the same side of the body as another structure is described as:",
        "options": [
            "Ipsilateral",
            "Contralateral",
            "Bilateral",
            "Unilateral"
        ],
        "answer_index": 0,
        "explanation": (
            "Ipsilateral means on the same side of the body. Contralateral means on the opposite side. "
            "Bilateral refers to paired structures, and unilateral to a structure present on one side only."
        ),
    },

    # =================
    # Membrane Transport
    # =================
    {
        "id": 210,
        "topic": "Membrane Transport",
        "question": "Which factor does NOT directly influence the rate of simple diffusion of a solute across a membrane?",
        "options": [
            "Availability of carrier proteins",
            "Concentration gradient",
            "Membrane permeability",
            "Surface area of the membrane"
        ],
        "answer_index": 0,
        "explanation": (
            "Simple diffusion does not use carrier proteins, so their availability does not affect its rate. "
            "According to Fick's law, rate depends on concentration gradient, permeability, and surface area."
        ),
    },
    {
        "id": 211,
        "topic": "Membrane Transport",
        "question": "Secondary active transport:",
        "options": [
            "Uses energy stored in ion gradients created by primary active transport",
            "Consumes ATP directly at the carrier protein",
            "Moves solutes only down their concentration gradients",
            "Occurs only through simple diffusion"
        ],
        "answer_index": 0,
        "explanation": (
            "Secondary active transport uses the potential energy of an existing ion gradient "
            "(e.g. Na⁺ gradient created by Na⁺/K⁺-ATPase) to move another solute uphill. "
            "It does not hydrolyse ATP directly at the carrier."
        ),
    },
    {
        "id": 212,
        "topic": "Membrane Transport",
        "question": "Which of the following is an example of a symporter?",
        "options": [
            "Na⁺–glucose cotransporter in the intestinal epithelium",
            "Na⁺/K⁺-ATPase pump",
            "Na⁺/Ca²⁺ exchanger",
            "Cl⁻/HCO₃⁻ exchanger"
        ],
        "answer_index": 0,
        "explanation": (
            "The Na⁺–glucose cotransporter carries Na⁺ and glucose in the same direction across the membrane "
            "and is a classic example of a symporter using secondary active transport."
        ),
    },
    {
        "id": 213,
        "topic": "Membrane Transport",
        "question": "Osmosis is best defined as:",
        "options": [
            "Movement of water across a semipermeable membrane from low solute concentration to high solute concentration",
            "Movement of solute from high concentration to low concentration",
            "Active transport of ions against their gradient",
            "Exocytosis of vesicles from the cell"
        ],
        "answer_index": 0,
        "explanation": (
            "Osmosis is the passive movement of water across a semipermeable membrane from a region of lower "
            "solute concentration (higher water potential) to higher solute concentration."
        ),
    },
    {
        "id": 214,
        "topic": "Membrane Transport",
        "question": "Which statement about facilitated diffusion is TRUE?",
        "options": [
            "It exhibits a maximum transport rate (Tmax) at high substrate concentration",
            "It can transport solutes against their concentration gradient",
            "It always requires the direct use of ATP",
            "It is independent of the number of carrier proteins"
        ],
        "answer_index": 0,
        "explanation": (
            "Facilitated diffusion uses carrier proteins and shows saturation (Tmax) when all carriers are occupied. "
            "It is still passive and moves solutes down their concentration gradient without using ATP directly."
        ),
    },

    # =====================
    # Epithelium & Glands
    # =====================
    {
        "id": 220,
        "topic": "Epithelium & Glands",
        "question": "Transitional epithelium is specially adapted for:",
        "options": [
            "Stretching to accommodate changes in volume",
            "Rapid gas exchange",
            "Mucus secretion only",
            "Absorption of nutrients"
        ],
        "answer_index": 0,
        "explanation": (
            "Transitional epithelium (urothelium) lines the urinary bladder and parts of the urinary tract. "
            "Its dome-shaped superficial cells allow stretching without tearing or losing integrity."
        ),
    },
    {
        "id": 221,
        "topic": "Epithelium & Glands",
        "question": "Which epithelium lines most of the gastrointestinal tract from the stomach to the rectum?",
        "options": [
            "Simple columnar epithelium",
            "Stratified squamous keratinised epithelium",
            "Simple cuboidal epithelium",
            "Pseudostratified ciliated columnar epithelium"
        ],
        "answer_index": 0,
        "explanation": (
            "Most of the GI tract from stomach to rectum is lined by simple columnar epithelium adapted for "
            "secretion and absorption. The oral cavity, oesophagus, and anal canal have stratified squamous epithelium."
        ),
    },
    {
        "id": 222,
        "topic": "Epithelium & Glands",
        "question": "Endocrine glands are characterised by:",
        "options": [
            "Lack of ducts and secretion of hormones into the bloodstream",
            "Presence of ducts opening onto body surfaces",
            "Secretion of only serous fluid",
            "Release of their whole cells as secretion"
        ],
        "answer_index": 0,
        "explanation": (
            "Endocrine glands are ductless and secrete hormones directly into the interstitial fluid and blood. "
            "Exocrine glands use ducts to deliver secretions to body surfaces or cavities."
        ),
    },
    {
        "id": 223,
        "topic": "Epithelium & Glands",
        "question": "Goblet cells are best described as:",
        "options": [
            "Unicellular mucous-secreting exocrine glands",
            "Multicellular serous glands",
            "Endocrine cells secreting hormones",
            "Holocrine glands in the skin"
        ],
        "answer_index": 0,
        "explanation": (
            "Goblet cells are unicellular exocrine glands that secrete mucus. "
            "They are found in the respiratory and intestinal epithelium."
        ),
    },
    {
        "id": 224,
        "topic": "Epithelium & Glands",
        "question": "A gland with a branched duct system and secretory units that are flask-shaped is called:",
        "options": [
            "Compound acinar gland",
            "Simple tubular gland",
            "Compound tubular gland",
            "Simple coiled tubular gland"
        ],
        "answer_index": 0,
        "explanation": (
            "Acinar (or alveolar) glands have sac-like secretory units. A branched duct system makes it a compound gland. "
            "So a compound acinar gland has multiple branched ducts ending in acini."
        ),
    },

    # =====================================
    # Connective Tissue, Cartilage & Bone
    # =====================================
    {
        "id": 230,
        "topic": "Connective Tissue, Cartilage & Bone",
        "question": "Which connective tissue cell type is primarily responsible for producing fibres and ground substance?",
        "options": [
            "Fibroblast",
            "Mast cell",
            "Macrophage",
            "Plasma cell"
        ],
        "answer_index": 0,
        "explanation": (
            "Fibroblasts are the principal cells of most connective tissues and synthesise collagen, elastic fibres, "
            "reticular fibres, and ground substance components."
        ),
    },
    {
        "id": 231,
        "topic": "Connective Tissue, Cartilage & Bone",
        "question": "Which type of cartilage is found in the external ear (pinna) and epiglottis?",
        "options": [
            "Elastic cartilage",
            "Hyaline cartilage",
            "Fibrocartilage",
            "Articular cartilage only"
        ],
        "answer_index": 0,
        "explanation": (
            "Elastic cartilage contains abundant elastic fibres in addition to type II collagen. "
            "It is found in the pinna, epiglottis, and auditory tube, allowing flexibility and shape retention."
        ),
    },
    {
        "id": 232,
        "topic": "Connective Tissue, Cartilage & Bone",
        "question": "Which bone cell type is responsible for bone resorption?",
        "options": [
            "Osteoclast",
            "Osteoblast",
            "Osteocyte",
            "Osteogenic cell"
        ],
        "answer_index": 0,
        "explanation": (
            "Osteoclasts are large multinucleated cells derived from the monocyte–macrophage lineage. "
            "They break down bone matrix during growth, remodelling, and calcium regulation."
        ),
    },
    {
        "id": 233,
        "topic": "Connective Tissue, Cartilage & Bone",
        "question": "Spongy (cancellous) bone is characterised by:",
        "options": [
            "A network of trabeculae with marrow spaces",
            "Solid concentric lamellae with central canals only",
            "Absence of bone marrow",
            "Being found only in long bone shafts"
        ],
        "answer_index": 0,
        "explanation": (
            "Spongy bone consists of a lattice of trabeculae with interconnecting marrow spaces. "
            "It is prominent in epiphyses of long bones and in flat bones like the pelvis and skull."
        ),
    },
    {
        "id": 234,
        "topic": "Connective Tissue, Cartilage & Bone",
        "question": "Intramembranous ossification is the process by which:",
        "options": [
            "Flat bones of the skull develop directly from mesenchyme",
            "Long bones develop through a cartilage model",
            "Articular cartilage is replaced by bone",
            "Secondary ossification centres form in epiphyses"
        ],
        "answer_index": 0,
        "explanation": (
            "Intramembranous ossification involves direct bone formation from mesenchymal tissue and forms "
            "many flat bones of the skull and the clavicle. Long bones mainly form by endochondral ossification."
        ),
    },

    # =================
    # Joints & Muscle
    # =================
    {
        "id": 240,
        "topic": "Joints & Muscle",
        "question": "Which of the following is an example of a fibrous joint?",
        "options": [
            "Suture between skull bones",
            "Pubic symphysis",
            "Shoulder joint",
            "Intervertebral joint between vertebral bodies"
        ],
        "answer_index": 0,
        "explanation": (
            "Sutures between skull bones are fibrous joints with very little movement. "
            "Pubic symphysis and intervertebral joints are secondary cartilaginous joints, "
            "and the shoulder is a synovial joint."
        ),
    },
    {
        "id": 241,
        "topic": "Joints & Muscle",
        "question": "A primary cartilaginous joint (synchondrosis) is characterised by:",
        "options": [
            "Union of bones by hyaline cartilage",
            "Union of bones by fibrocartilage",
            "Presence of a joint cavity and synovial membrane",
            "Being freely movable in all directions"
        ],
        "answer_index": 0,
        "explanation": (
            "Primary cartilaginous joints are united by hyaline cartilage (e.g. epiphyseal growth plates, "
            "first costochondral joint). Secondary cartilaginous joints use fibrocartilage (e.g. pubic symphysis)."
        ),
    },
    {
        "id": 242,
        "topic": "Joints & Muscle",
        "question": "Which statement about skeletal muscle is TRUE?",
        "options": [
            "It is striated and under voluntary control",
            "It is non-striated and involuntary",
            "It has intercalated discs between cells",
            "It is found in the walls of hollow viscera only"
        ],
        "answer_index": 0,
        "explanation": (
            "Skeletal muscle fibres are long, striated, multinucleated, and under voluntary control. "
            "Cardiac muscle is striated with intercalated discs; smooth muscle is non-striated."
        ),
    },
    {
        "id": 243,
        "topic": "Joints & Muscle",
        "question": "The connective tissue layer that surrounds an individual skeletal muscle fibre is called:",
        "options": [
            "Endomysium",
            "Perimysium",
            "Epimysium",
            "Periosteum"
        ],
        "answer_index": 0,
        "explanation": (
            "Endomysium surrounds individual muscle fibres. Perimysium surrounds bundles (fascicles), "
            "and epimysium surrounds the whole muscle."
        ),
    },
    {
        "id": 244,
        "topic": "Joints & Muscle",
        "question": "A motor unit consists of:",
        "options": [
            "A motor neuron and all the muscle fibres it innervates",
            "A sensory neuron and its receptor endings",
            "A group of adjacent sarcomeres",
            "All the muscles acting across a joint"
        ],
        "answer_index": 0,
        "explanation": (
            "A motor unit is one alpha motor neuron and all the skeletal muscle fibres it supplies. "
            "Activation of a motor unit causes all its fibres to contract together."
        ),
    },

    # ====================================
    # Nervous System (CNS & PNS general)
    # ====================================
    {
        "id": 250,
        "topic": "Nervous System (CNS & PNS)",
        "question": "The grey matter of the spinal cord is arranged:",
        "options": [
            "Centrally in an H-shaped (butterfly) pattern",
            "Peripherally as a continuous outer layer",
            "Only in the posterior columns",
            "Only in the anterior columns"
        ],
        "answer_index": 0,
        "explanation": (
            "In the spinal cord, grey matter is central, forming an H-shaped region containing neuronal cell bodies. "
            "White matter surrounds it as columns containing ascending and descending tracts."
        ),
    },
    {
        "id": 251,
        "topic": "Nervous System (CNS & PNS)",
        "question": "Which neuroglial cell forms myelin in the peripheral nervous system?",
        "options": [
            "Schwann cell",
            "Oligodendrocyte",
            "Astrocyte",
            "Microglial cell"
        ],
        "answer_index": 0,
        "explanation": (
            "Schwann cells form myelin sheaths around peripheral axons. Oligodendrocytes myelinate CNS axons."
        ),
    },
    {
        "id": 252,
        "topic": "Nervous System (CNS & PNS)",
        "question": "Which of the following is a function of cerebrospinal fluid (CSF)?",
        "options": [
            "Mechanical protection and cushioning of the CNS",
            "Production of myelin for axons",
            "Generation of action potentials",
            "Transmission of impulses at neuromuscular junctions"
        ],
        "answer_index": 0,
        "explanation": (
            "CSF provides mechanical protection, buoyancy, and a stable chemical environment for the brain and spinal cord."
        ),
    },
    {
        "id": 253,
        "topic": "Nervous System (CNS & PNS)",
        "question": "Association fibres in the brain connect:",
        "options": [
            "Areas within the same cerebral hemisphere",
            "The two cerebral hemispheres",
            "The cortex with lower centres such as the spinal cord",
            "The cerebellum with the spinal cord only"
        ],
        "answer_index": 0,
        "explanation": (
            "Association fibres interconnect cortical areas within the same hemisphere. "
            "Commissural fibres (e.g. corpus callosum) connect the two hemispheres, "
            "while projection fibres connect the cortex with lower centres."
        ),
    },
    {
        "id": 254,
        "topic": "Nervous System (CNS & PNS)",
        "question": "The meninges, from outermost to innermost, are:",
        "options": [
            "Dura mater, arachnoid mater, pia mater",
            "Pia mater, arachnoid mater, dura mater",
            "Arachnoid mater, dura mater, pia mater",
            "Dura mater, pia mater, arachnoid mater"
        ],
        "answer_index": 0,
        "explanation": (
            "The meninges are three protective membranes: outer dura mater, middle arachnoid mater, and inner pia mater "
            "closely adhering to the brain and spinal cord."
        ),
    },

    # ==========
    # ANS
    # ==========
    {
        "id": 260,
        "topic": "ANS",
        "question": "Which neurotransmitter is released by most postganglionic sympathetic neurons?",
        "options": [
            "Noradrenaline (norepinephrine)",
            "Acetylcholine only",
            "Dopamine",
            "Serotonin"
        ],
        "answer_index": 0,
        "explanation": (
            "Most postganglionic sympathetic neurons release noradrenaline at their effector organs. "
            "An important exception is those supplying sweat glands, which release acetylcholine."
        ),
    },
    {
        "id": 261,
        "topic": "ANS",
        "question": "Parasympathetic fibres in the vagus nerve mainly supply:",
        "options": [
            "Thoracic and most abdominal organs",
            "Lower limb muscles",
            "Parotid salivary gland only",
            "Adrenal medulla"
        ],
        "answer_index": 0,
        "explanation": (
            "The vagus nerve (cranial nerve X) carries parasympathetic fibres to the heart, lungs, and much of the GI tract "
            "up to the proximal colon."
        ),
    },
    {
        "id": 262,
        "topic": "ANS",
        "question": "A typical sympathetic response includes:",
        "options": [
            "Increased heart rate and blood pressure",
            "Increased saliva production with watery secretions",
            "Increased gastrointestinal motility",
            "Constriction of the pupil"
        ],
        "answer_index": 0,
        "explanation": (
            "Sympathetic activation ('fight or flight') increases heart rate, blood pressure, and blood flow to skeletal muscle, "
            "while decreasing GI activity and causing pupillary dilation."
        ),
    },
    {
        "id": 263,
        "topic": "ANS",
        "question": "Parasympathetic preganglionic neurons have their cell bodies in:",
        "options": [
            "Brainstem nuclei and sacral spinal cord segments",
            "Thoracic and lumbar spinal cord segments T1–L2",
            "Dorsal root ganglia",
            "Sympathetic chain ganglia"
        ],
        "answer_index": 0,
        "explanation": (
            "Parasympathetic outflow is craniosacral, arising from certain brainstem nuclei (CN III, VII, IX, X) "
            "and sacral segments S2–S4."
        ),
    },
    {
        "id": 264,
        "topic": "ANS",
        "question": "Sympathetic chain (paravertebral) ganglia are located:",
        "options": [
            "On either side of the vertebral column",
            "Within the dorsal horn of the spinal cord",
            "In the walls of the target organs only",
            "Inside the cranial cavity only"
        ],
        "answer_index": 0,
        "explanation": (
            "Sympathetic chain ganglia form a longitudinal chain on either side of the vertebral bodies. "
            "Parasympathetic ganglia are often located near or within target organs."
        ),
    },

    # ===========================
    # Heart & Blood Vessels
    # ===========================
    {
        "id": 270,
        "topic": "Heart & Blood Vessels",
        "question": "The right atrium receives deoxygenated blood from all of the following EXCEPT:",
        "options": [
            "Pulmonary veins",
            "Superior vena cava",
            "Inferior vena cava",
            "Coronary sinus"
        ],
        "answer_index": 0,
        "explanation": (
            "Pulmonary veins carry oxygenated blood from the lungs to the left atrium. "
            "The right atrium receives deoxygenated blood from the superior vena cava, inferior vena cava, and coronary sinus."
        ),
    },
    {
        "id": 271,
        "topic": "Heart & Blood Vessels",
        "question": "Which structure electrically connects the atria to the ventricles in the normal heart?",
        "options": [
            "Atrioventricular (AV) bundle (Bundle of His)",
            "SA node",
            "Purkinje fibres only",
            "Interatrial septum"
        ],
        "answer_index": 0,
        "explanation": (
            "The AV bundle is the only normal electrical connection between atria and ventricles, "
            "carrying impulses from the AV node to the bundle branches."
        ),
    },
    {
        "id": 272,
        "topic": "Heart & Blood Vessels",
        "question": "Which artery usually supplies the SA node in the majority of individuals?",
        "options": [
            "Right coronary artery",
            "Left coronary artery",
            "Left circumflex artery only",
            "Anterior interventricular (LAD) artery"
        ],
        "answer_index": 0,
        "explanation": (
            "In most people, the SA nodal branch arises from the right coronary artery. "
            "In a smaller percentage, it can arise from the left circumflex artery."
        ),
    },
    {
        "id": 273,
        "topic": "Heart & Blood Vessels",
        "question": "Muscular arteries are characterised by:",
        "options": [
            "A prominent tunica media rich in smooth muscle cells",
            "Dominance of elastic lamellae in the tunica media",
            "Absence of internal elastic lamina",
            "Presence of valves similar to veins"
        ],
        "answer_index": 0,
        "explanation": (
            "Muscular (distributing) arteries have a thick tunica media with many smooth muscle cells "
            "and a distinct internal elastic lamina. Elastic arteries have abundant elastic lamellae."
        ),
    },
    {
        "id": 274,
        "topic": "Heart & Blood Vessels",
        "question": "Veins differ from arteries in that veins typically:",
        "options": [
            "Have thinner walls and larger lumina",
            "Have thicker tunica media",
            "Always carry oxygenated blood",
            "Lack valves completely"
        ],
        "answer_index": 0,
        "explanation": (
            "Compared with arteries, veins usually have thinner walls, less smooth muscle, and larger lumina. "
            "Many medium-sized veins possess valves to prevent backflow."
        ),
    },

    # =====================
    # Lymphatic System
    # =====================
    {
        "id": 280,
        "topic": "Lymphatic System",
        "question": "The thoracic duct drains lymph from:",
        "options": [
            "Most of the body below the diaphragm and the left upper quadrant",
            "Only the right upper limb and right side of head and neck",
            "Only the gastrointestinal tract",
            "Only the lungs"
        ],
        "answer_index": 0,
        "explanation": (
            "The thoracic duct drains lymph from both lower limbs, abdomen, left thorax, left upper limb, and left side of head and neck. "
            "The right lymphatic duct drains the right upper limb, right thorax, and right side of head and neck."
        ),
    },
    {
        "id": 281,
        "topic": "Lymphatic System",
        "question": "White pulp of the spleen is mainly involved in:",
        "options": [
            "Immune functions and lymphocyte activation",
            "Filtration of old red blood cells only",
            "Production of bile",
            "Secretion of digestive enzymes"
        ],
        "answer_index": 0,
        "explanation": (
            "White pulp consists of lymphoid tissue around central arteries and is involved in immune responses. "
            "Red pulp filters blood and removes old or damaged red blood cells."
        ),
    },
    {
        "id": 282,
        "topic": "Lymphatic System",
        "question": "MALT (mucosa-associated lymphoid tissue) includes all of the following EXCEPT:",
        "options": [
            "Bone marrow",
            "Tonsils",
            "Peyer’s patches",
            "Appendix"
        ],
        "answer_index": 0,
        "explanation": (
            "MALT refers to lymphoid tissue in mucosal sites such as tonsils, Peyer’s patches in the ileum, and the appendix. "
            "Bone marrow is a primary lymphoid organ but not considered MALT."
        ),
    },
    {
        "id": 283,
        "topic": "Lymphatic System",
        "question": "Enlarged, tender lymph nodes are most often a sign of:",
        "options": [
            "Active infection in their drainage area",
            "Normal anatomical variation",
            "Complete absence of lymph flow",
            "Dehydration only"
        ],
        "answer_index": 0,
        "explanation": (
            "Lymph nodes often enlarge and become tender during active infection in the region they drain, "
            "due to proliferation of immune cells and inflammation."
        ),
    },
    {
        "id": 284,
        "topic": "Lymphatic System",
        "question": "Lymph is best described as:",
        "options": [
            "Tissue fluid that has entered lymphatic capillaries",
            "Fluid filtered directly from glomeruli",
            "Secretions of endocrine glands",
            "Plasma within blood vessels"
        ],
        "answer_index": 0,
        "explanation": (
            "Lymph originates as interstitial (tissue) fluid that enters lymphatic capillaries. "
            "It eventually returns to the venous system via lymphatic ducts."
        ),
    },

    # =====================
    # Respiratory System
    # =====================
    {
        "id": 290,
        "topic": "Respiratory System",
        "question": "The trachea is kept open mainly by:",
        "options": [
            "C-shaped rings of hyaline cartilage",
            "Complete rings of elastic cartilage",
            "Smooth muscle only",
            "Bony rings"
        ],
        "answer_index": 0,
        "explanation": (
            "The trachea has C-shaped hyaline cartilage rings that prevent collapse while allowing the oesophagus to expand posteriorly."
        ),
    },
    {
        "id": 291,
        "topic": "Respiratory System",
        "question": "The conducting portion of the respiratory system includes all of the following EXCEPT:",
        "options": [
            "Respiratory bronchioles",
            "Trachea",
            "Bronchi",
            "Terminal bronchioles"
        ],
        "answer_index": 0,
        "explanation": (
            "Respiratory bronchioles are part of the respiratory portion, where some gas exchange occurs. "
            "The conducting portion includes nasal cavity, pharynx, larynx, trachea, bronchi, and terminal bronchioles."
        ),
    },
    {
        "id": 292,
        "topic": "Respiratory System",
        "question": "Type II pneumocytes are primarily responsible for:",
        "options": [
            "Producing surfactant",
            "Forming the thin gas-exchange barrier",
            "Phagocytosing dust particles",
            "Producing mucus"
        ],
        "answer_index": 0,
        "explanation": (
            "Type II pneumocytes secrete pulmonary surfactant, which reduces surface tension in alveoli. "
            "Type I pneumocytes form most of the thin gas-exchange surface; alveolar macrophages phagocytose debris."
        ),
    },
    {
        "id": 293,
        "topic": "Respiratory System",
        "question": "The diaphragm is innervated by the:",
        "options": [
            "Phrenic nerve (C3–C5)",
            "Vagus nerve",
            "Intercostal nerves only",
            "Accessory nerve"
        ],
        "answer_index": 0,
        "explanation": (
            "The phrenic nerve (C3, C4, C5) supplies motor innervation to the diaphragm. "
            "A classic phrase is 'C3, 4, 5 keep the diaphragm alive'."
        ),
    },
    {
        "id": 294,
        "topic": "Respiratory System",
        "question": "In quiet inspiration, which of the following is the main muscle of respiration?",
        "options": [
            "Diaphragm",
            "Internal intercostals",
            "Abdominal muscles",
            "Sternocleidomastoid"
        ],
        "answer_index": 0,
        "explanation": (
            "During quiet breathing, the diaphragm is the primary muscle of inspiration. "
            "External intercostals also assist; accessory muscles are recruited during deep or laboured breathing."
        ),
    },

    # =================
    # Urinary System
    # =================
    {
        "id": 300,
        "topic": "Urinary System",
        "question": "The renal cortex contains all of the following EXCEPT:",
        "options": [
            "Renal pyramids",
            "Renal corpuscles",
            "Proximal convoluted tubules",
            "Distal convoluted tubules"
        ],
        "answer_index": 0,
        "explanation": (
            "Renal pyramids are located in the medulla. The cortex contains renal corpuscles and the convoluted segments of tubules."
        ),
    },
    {
        "id": 301,
        "topic": "Urinary System",
        "question": "Which part of the nephron is primarily responsible for filtration of blood?",
        "options": [
            "Glomerulus within Bowman's capsule",
            "Proximal convoluted tubule",
            "Loop of Henle",
            "Collecting duct"
        ],
        "answer_index": 0,
        "explanation": (
            "Filtration occurs at the renal corpuscle: blood passes through the glomerular capillaries into Bowman's space, "
            "forming the filtrate."
        ),
    },
    {
        "id": 302,
        "topic": "Urinary System",
        "question": "The ureters pass into the bladder:",
        "options": [
            "Obliquely through its wall to form a functional valve",
            "Directly and vertically through its floor",
            "Only through the posterior surface without obliquity",
            "Through the urethra first"
        ],
        "answer_index": 0,
        "explanation": (
            "The ureters enter the bladder obliquely through the wall. As the bladder fills and the wall stretches, "
            "this obliquity helps prevent reflux of urine."
        ),
    },
    {
        "id": 303,
        "topic": "Urinary System",
        "question": "The trigone of the urinary bladder is defined by:",
        "options": [
            "Two ureteric openings and the internal urethral orifice",
            "The openings of the urethra only",
            "The ureteric openings and the external urethral orifice",
            "The superior surface of the bladder"
        ],
        "answer_index": 0,
        "explanation": (
            "The trigone is a smooth triangular area on the posterior bladder wall, bounded by the two ureteric orifices "
            "and the internal urethral orifice."
        ),
    },
    {
        "id": 304,
        "topic": "Urinary System",
        "question": "Which hormone mainly increases water reabsorption in the collecting ducts?",
        "options": [
            "Antidiuretic hormone (ADH)",
            "Aldosterone",
            "Insulin",
            "Thyroxine"
        ],
        "answer_index": 0,
        "explanation": (
            "ADH increases the permeability of the collecting ducts to water, allowing more water reabsorption and "
            "concentrated urine. Aldosterone mainly promotes Na⁺ reabsorption and K⁺ secretion."
        ),
    },

    # =================
    # Endocrine System
    # =================
    {
        "id": 310,
        "topic": "Endocrine System",
        "question": "The anterior pituitary (adenohypophysis) develops embryologically from:",
        "options": [
            "An upward growth of oral ectoderm (Rathke's pouch)",
            "A downward extension of neural tissue",
            "Mesoderm within the sella turcica",
            "Endoderm of the pharyngeal pouches"
        ],
        "answer_index": 0,
        "explanation": (
            "The anterior pituitary arises from Rathke's pouch, an upward evagination of oral ectoderm. "
            "The posterior pituitary is a downward extension of the hypothalamus."
        ),
    },
    {
        "id": 311,
        "topic": "Endocrine System",
        "question": "Which gland secretes melatonin and helps regulate circadian rhythms?",
        "options": [
            "Pineal gland",
            "Thyroid gland",
            "Adrenal cortex",
            "Pancreas"
        ],
        "answer_index": 0,
        "explanation": (
            "The pineal gland secretes melatonin, which influences circadian (day–night) rhythms and seasonal changes."
        ),
    },
    {
        "id": 312,
        "topic": "Endocrine System",
        "question": "Which hormone is produced by the beta cells of the pancreatic islets?",
        "options": [
            "Insulin",
            "Glucagon",
            "Somatostatin",
            "Adrenaline"
        ],
        "answer_index": 0,
        "explanation": (
            "Beta cells of the islets of Langerhans secrete insulin, which lowers blood glucose. "
            "Alpha cells secrete glucagon."
        ),
    },
    {
        "id": 313,
        "topic": "Endocrine System",
        "question": "Which of the following is a steroid hormone?",
        "options": [
            "Cortisol",
            "Insulin",
            "Adrenaline",
            "Growth hormone"
        ],
        "answer_index": 0,
        "explanation": (
            "Cortisol is a steroid hormone produced by the adrenal cortex. "
            "Insulin and growth hormone are peptide hormones; adrenaline is a catecholamine."
        ),
    },
    {
        "id": 314,
        "topic": "Endocrine System",
        "question": "Parathyroid hormone (PTH) mainly acts to:",
        "options": [
            "Increase blood calcium levels",
            "Decrease blood calcium levels",
            "Increase insulin secretion",
            "Stimulate thyroid hormone release only"
        ],
        "answer_index": 0,
        "explanation": (
            "PTH raises blood calcium by stimulating bone resorption, increasing renal Ca²⁺ reabsorption, "
            "and enhancing activation of vitamin D, which increases intestinal Ca²⁺ absorption."
        ),
    },

    # ============================
    # Male Reproductive System
    # ============================
    {
        "id": 320,
        "topic": "Male Reproductive System",
        "question": "Leydig cells in the testis mainly secrete:",
        "options": [
            "Testosterone",
            "FSH",
            "Progesterone",
            "Prolactin"
        ],
        "answer_index": 0,
        "explanation": (
            "Leydig (interstitial) cells, located between seminiferous tubules, secrete testosterone under stimulation by LH."
        ),
    },
    {
        "id": 321,
        "topic": "Male Reproductive System",
        "question": "Which structure stores sperm and allows them to mature?",
        "options": [
            "Epididymis",
            "Seminal vesicle",
            "Prostate gland",
            "Bulbourethral gland"
        ],
        "answer_index": 0,
        "explanation": (
            "The epididymis stores sperm for several weeks and is the site of sperm maturation and acquisition of motility."
        ),
    },
    {
        "id": 322,
        "topic": "Male Reproductive System",
        "question": "Which gland contributes a fructose-rich secretion that nourishes sperm?",
        "options": [
            "Seminal vesicle",
            "Prostate gland",
            "Bulbourethral gland",
            "Pituitary gland"
        ],
        "answer_index": 0,
        "explanation": (
            "The seminal vesicles produce a yellowish, alkaline, fructose-rich fluid that forms a major part of semen."
        ),
    },
    {
        "id": 323,
        "topic": "Male Reproductive System",
        "question": "The pampiniform plexus in the spermatic cord functions mainly to:",
        "options": [
            "Help regulate the temperature of the testis",
            "Store sperm prior to ejaculation",
            "Produce testosterone",
            "Serve as a lymphatic drainage pathway"
        ],
        "answer_index": 0,
        "explanation": (
            "The pampiniform venous plexus surrounds the testicular artery and acts as a counter-current heat exchanger, "
            "cooling arterial blood to maintain optimal testicular temperature."
        ),
    },
    {
        "id": 324,
        "topic": "Male Reproductive System",
        "question": "Which structure passes through the inguinal canal in the male?",
        "options": [
            "Spermatic cord",
            "Ureter",
            "Femoral artery",
            "Obturator nerve"
        ],
        "answer_index": 0,
        "explanation": (
            "The spermatic cord, containing the vas deferens, vessels, nerves, and lymphatics, passes through the inguinal canal "
            "to reach the testis."
        ),
    },

    # ==============================
    # Female Reproductive System
    # ==============================
    {
        "id": 330,
        "topic": "Female Reproductive System",
        "question": "Which ligament contains the ovarian vessels?",
        "options": [
            "Suspensory ligament of the ovary",
            "Round ligament of the uterus",
            "Ovarian ligament",
            "Broad ligament only"
        ],
        "answer_index": 0,
        "explanation": (
            "The suspensory ligament of the ovary (infundibulopelvic ligament) carries the ovarian artery and vein "
            "from the lateral pelvic wall to the ovary."
        ),
    },
    {
        "id": 331,
        "topic": "Female Reproductive System",
        "question": "The part of the uterine tube that opens into the peritoneal cavity near the ovary is the:",
        "options": [
            "Infundibulum",
            "Ampulla",
            "Isthmus",
            "Intramural part"
        ],
        "answer_index": 0,
        "explanation": (
            "The infundibulum is the funnel-shaped lateral end of the uterine tube with fimbriae that open near the ovary."
        ),
    },
    {
        "id": 332,
        "topic": "Female Reproductive System",
        "question": "The uterine cervix projects into the vagina and forms:",
        "options": [
            "Anterior, posterior, and lateral fornices",
            "Only an anterior fornix",
            "Only a posterior fornix",
            "No fornices at all"
        ],
        "answer_index": 0,
        "explanation": (
            "The vaginal part of the cervix protrudes into the upper vagina, forming anterior, posterior, and two lateral fornices. "
            "The posterior fornix is the deepest."
        ),
    },
    {
        "id": 333,
        "topic": "Female Reproductive System",
        "question": "Which layer of the uterine wall undergoes cyclic changes during the menstrual cycle?",
        "options": [
            "Endometrium",
            "Myometrium",
            "Perimetrium",
            "Peritoneum of the broad ligament"
        ],
        "answer_index": 0,
        "explanation": (
            "The endometrium (mucosal lining) of the body of the uterus undergoes cyclic proliferation, secretion, and shedding "
            "during the menstrual cycle."
        ),
    },
    {
        "id": 334,
        "topic": "Female Reproductive System",
        "question": "The vulva does NOT include which of the following structures?",
        "options": [
            "Uterine body",
            "Labia majora",
            "Labia minora",
            "Clitoris"
        ],
        "answer_index": 0,
        "explanation": (
            "The vulva includes the external female genital structures (mons pubis, labia majora, labia minora, clitoris, vestibule, etc.). "
            "The uterine body is an internal pelvic organ, not part of the vulva."
        ),
    },

    # ====================================
    # Cell Division & Early Embryology
    # ====================================
    {
        "id": 340,
        "topic": "Cell Division & Early Embryology",
        "question": "During which stage of meiosis does crossing over of homologous chromosomes mainly occur?",
        "options": [
            "Prophase I",
            "Metaphase I",
            "Anaphase II",
            "Telophase II"
        ],
        "answer_index": 0,
        "explanation": (
            "Crossing over and genetic recombination occur mainly during prophase I of meiosis, particularly in the pachytene stage."
        ),
    },
    {
        "id": 341,
        "topic": "Cell Division & Early Embryology",
        "question": "The blastocyst is characterised by:",
        "options": [
            "A fluid-filled cavity and an inner cell mass",
            "A solid mass of cells without a cavity",
            "A bilaminar embryonic disc",
            "Presence of three germ layers"
        ],
        "answer_index": 0,
        "explanation": (
            "The blastocyst has a central cavity (blastocoel), an inner cell mass (embryoblast), and an outer trophoblast. "
            "Gastrulation later forms the three germ layers."
        ),
    },
    {
        "id": 342,
        "topic": "Cell Division & Early Embryology",
        "question": "The bilaminar embryonic disc consists of:",
        "options": [
            "Epiblast and hypoblast",
            "Ectoderm and mesoderm",
            "Mesoderm and endoderm",
            "Ectoderm, mesoderm, and endoderm"
        ],
        "answer_index": 0,
        "explanation": (
            "In the second week, the embryoblast differentiates into a bilaminar disc with epiblast (dorsal) and hypoblast (ventral) layers."
        ),
    },
    {
        "id": 343,
        "topic": "Cell Division & Early Embryology",
        "question": "Gastrulation is the process by which:",
        "options": [
            "The three primary germ layers are formed from the epiblast",
            "The morula becomes a blastocyst",
            "The neural tube forms from the neural plate",
            "The zygote undergoes the first cleavage division"
        ],
        "answer_index": 0,
        "explanation": (
            "Gastrulation reorganises the bilaminar disc into a trilaminar disc with ectoderm, mesoderm, and endoderm derived from epiblast cells."
        ),
    },
    {
        "id": 344,
        "topic": "Cell Division & Early Embryology",
        "question": "The notochord is important embryologically because it:",
        "options": [
            "Defines the future axis of the embryo and induces neural tube formation",
            "Forms the definitive spinal cord",
            "Forms the heart tube",
            "Becomes the adult vertebral column directly"
        ],
        "answer_index": 0,
        "explanation": (
            "The notochord is a midline mesodermal structure that defines the longitudinal axis and induces overlying ectoderm "
            "to form the neural plate and neural tube. It later contributes to the nucleus pulposus."
        ),
    },
]

EXTRA_QUESTIONS = [
    # =========================
    # Anatomical Terms & Planes
    # =========================
    {
        "id": 400,
        "topic": "Anatomical Terms & Planes",
        "question": "Which of the following terms refers to a structure located closer to the surface of the body?",
        "options": [
            "Superficial",
            "Deep",
            "Inferior",
            "Proximal"
        ],
        "answer_index": 0,
        "explanation": (
            "Superficial means closer to the surface of the body. Deep means further away from the surface. "
            "Inferior refers to a lower position, and proximal refers to nearer the trunk or point of origin."
        ),
    },
    {
        "id": 401,
        "topic": "Anatomical Terms & Planes",
        "question": "Which movement describes turning the palm from facing anteriorly to facing posteriorly?",
        "options": [
            "Pronation",
            "Supination",
            "Flexion",
            "Abduction"
        ],
        "answer_index": 0,
        "explanation": (
            "Pronation of the forearm turns the palm from facing forwards (anatomical position) to facing backwards. "
            "Supination is the opposite movement."
        ),
    },
    {
        "id": 402,
        "topic": "Anatomical Terms & Planes",
        "question": "The term 'bilateral' is best used to describe:",
        "options": [
            "Paired structures found on both sides, such as kidneys",
            "A structure on only one side of the body",
            "Structures on opposite sides of the body",
            "The relationship of superficial to deep structures"
        ],
        "answer_index": 0,
        "explanation": (
            "Bilateral structures are paired and present on both sides of the body (e.g. kidneys, lungs). "
            "Unilateral means only on one side; contralateral refers to opposite sides."
        ),
    },
    {
        "id": 403,
        "topic": "Anatomical Terms & Planes",
        "question": "Which term correctly describes the position of the heart relative to the lungs?",
        "options": [
            "Medial",
            "Lateral",
            "Superficial",
            "Distal"
        ],
        "answer_index": 0,
        "explanation": (
            "The heart is medial to the lungs because it lies closer to the midline, whereas the lungs lie more laterally."
        ),
    },
    {
        "id": 404,
        "topic": "Anatomical Terms & Planes",
        "question": "An oblique plane:",
        "options": [
            "Cuts the body at an angle that is not purely sagittal, coronal, or transverse",
            "Always divides the body into equal halves",
            "Is the same as the median plane",
            "Only cuts through limbs"
        ],
        "answer_index": 0,
        "explanation": (
            "An oblique plane passes through the body at an angle that does not correspond exactly to sagittal, coronal, or transverse planes."
        ),
    },

    # =================
    # Membrane Transport
    # =================
    {
        "id": 410,
        "topic": "Membrane Transport",
        "question": "Which transport process requires vesicle formation to move materials into the cell?",
        "options": [
            "Endocytosis",
            "Simple diffusion",
            "Facilitated diffusion",
            "Primary active transport"
        ],
        "answer_index": 0,
        "explanation": (
            "Endocytosis involves the formation of vesicles from the plasma membrane to bring substances into the cell. "
            "The other processes move solutes across the membrane without vesicle formation."
        ),
    },
    {
        "id": 411,
        "topic": "Membrane Transport",
        "question": "In a cell, the Na⁺ gradient created by the Na⁺/K⁺-ATPase can be used to drive the uptake of glucose. This is an example of:",
        "options": [
            "Secondary active transport",
            "Primary active transport",
            "Simple diffusion",
            "Osmosis"
        ],
        "answer_index": 0,
        "explanation": (
            "The Na⁺/glucose cotransporter uses the energy stored in the Na⁺ gradient (established by Na⁺/K⁺-ATPase) "
            "to move glucose into the cell against its gradient, which is secondary active transport."
        ),
    },
    {
        "id": 412,
        "topic": "Membrane Transport",
        "question": "Which property is typical of carrier-mediated transport but NOT simple diffusion?",
        "options": [
            "Saturation at high solute concentrations",
            "Movement down a concentration gradient",
            "No requirement for a protein in the membrane",
            "No structural specificity"
        ],
        "answer_index": 0,
        "explanation": (
            "Carrier-mediated transport (facilitated diffusion or active transport) shows saturation when carriers are fully occupied. "
            "Simple diffusion does not saturate and does not require carriers."
        ),
    },
    {
        "id": 413,
        "topic": "Membrane Transport",
        "question": "A red blood cell placed in a hypotonic solution will:",
        "options": [
            "Gain water and may swell or burst",
            "Lose water and shrink",
            "Remain unchanged",
            "Actively pump water out to maintain its size"
        ],
        "answer_index": 0,
        "explanation": (
            "In a hypotonic solution, the extracellular solute concentration is lower, so water enters the cell by osmosis and the cell may swell or undergo haemolysis."
        ),
    },
    {
        "id": 414,
        "topic": "Membrane Transport",
        "question": "Which statement about aquaporins is TRUE?",
        "options": [
            "They are membrane proteins that selectively allow water to cross",
            "They actively pump water using ATP",
            "They transport ions such as Na⁺ and K⁺",
            "They are only found in red blood cells"
        ],
        "answer_index": 0,
        "explanation": (
            "Aquaporins are channel proteins that increase water permeability of the membrane, allowing rapid movement of water down its osmotic gradient."
        ),
    },

    # =====================
    # Epithelium & Glands
    # =====================
    {
        "id": 420,
        "topic": "Epithelium & Glands",
        "question": "Pseudostratified ciliated columnar epithelium with goblet cells typically lines the:",
        "options": [
            "Trachea",
            "Skin",
            "Urinary bladder",
            "Oesophagus"
        ],
        "answer_index": 0,
        "explanation": (
            "The respiratory tract (e.g. trachea and bronchi) is lined by pseudostratified ciliated columnar epithelium with goblet cells, which helps trap and move mucus."
        ),
    },
    {
        "id": 421,
        "topic": "Epithelium & Glands",
        "question": "Which characteristic is common to all epithelia?",
        "options": [
            "They rest on a basement membrane",
            "They contain abundant blood vessels",
            "They have a large amount of intercellular matrix",
            "They are always keratinised"
        ],
        "answer_index": 0,
        "explanation": (
            "All epithelia rest on a basement membrane and are avascular. Connective tissue has abundant extracellular matrix, not epithelium."
        ),
    },
    {
        "id": 422,
        "topic": "Epithelium & Glands",
        "question": "A simple tubular gland would be best described as a gland with:",
        "options": [
            "An unbranched duct and straight, tube-shaped secretory portion",
            "A branched duct and sac-like secretory units",
            "Several ducts converging into one main duct",
            "Multiple lobes separated by connective tissue septa only"
        ],
        "answer_index": 0,
        "explanation": (
            "Simple tubular glands have a single unbranched duct with a straight tubular secretory segment (e.g. glands in the colon)."
        ),
    },
    {
        "id": 423,
        "topic": "Epithelium & Glands",
        "question": "Holocrine secretion is characterised by:",
        "options": [
            "Disintegration of entire cells to release their contents",
            "Exocytosis of secretory granules without cell damage",
            "Pinching off of the apical cytoplasm only",
            "Transport of hormones into the bloodstream"
        ],
        "answer_index": 0,
        "explanation": (
            "In holocrine glands, whole cells fill with secretory product and then disintegrate, releasing their contents (e.g. sebaceous glands)."
        ),
    },
    {
        "id": 424,
        "topic": "Epithelium & Glands",
        "question": "Stratified squamous keratinised epithelium is mainly adapted for:",
        "options": [
            "Protection against mechanical and chemical stress",
            "Rapid absorption of nutrients",
            "Gas exchange",
            "Stretching during distension"
        ],
        "answer_index": 0,
        "explanation": (
            "Keratinised stratified squamous epithelium, as in the skin, provides strong protection against abrasion and water loss."
        ),
    },

    # =====================================
    # Connective Tissue, Cartilage & Bone
    # =====================================
    {
        "id": 430,
        "topic": "Connective Tissue, Cartilage & Bone",
        "question": "Reticular fibres are particularly abundant in the:",
        "options": [
            "Stroma of lymphoid organs such as lymph nodes and spleen",
            "Tendons and ligaments",
            "Articular cartilage",
            "Compact bone"
        ],
        "answer_index": 0,
        "explanation": (
            "Reticular fibres form delicate supporting networks in lymphoid organs like spleen and lymph nodes."
        ),
    },
    {
        "id": 431,
        "topic": "Connective Tissue, Cartilage & Bone",
        "question": "Dense regular connective tissue is best represented by:",
        "options": [
            "Tendons and ligaments",
            "Dermis of the skin",
            "Areolar tissue under epithelia",
            "Adipose tissue"
        ],
        "answer_index": 0,
        "explanation": (
            "Dense regular connective tissue has parallel bundles of collagen fibres, as in tendons and ligaments, adapted to resist tension in one direction."
        ),
    },
    {
        "id": 432,
        "topic": "Connective Tissue, Cartilage & Bone",
        "question": "Which statement about fibrocartilage is TRUE?",
        "options": [
            "It contains abundant type I collagen fibres and resists compression and tension",
            "It is covered by a well-defined perichondrium",
            "It lines articular surfaces of synovial joints",
            "It forms the epiglottis"
        ],
        "answer_index": 0,
        "explanation": (
            "Fibrocartilage has abundant type I collagen and is found in intervertebral discs and pubic symphysis. "
            "It usually lacks a perichondrium."
        ),
    },
    {
        "id": 433,
        "topic": "Connective Tissue, Cartilage & Bone",
        "question": "Osteocytes are located in:",
        "options": [
            "Lacunae within bone matrix",
            "Haversian canals only",
            "Periosteum only",
            "Bone marrow sinusoids"
        ],
        "answer_index": 0,
        "explanation": (
            "Osteocytes are mature bone cells residing in lacunae and connected by canaliculi."
        ),
    },
    {
        "id": 434,
        "topic": "Connective Tissue, Cartilage & Bone",
        "question": "In bone healing after a fracture, which event occurs earliest?",
        "options": [
            "Formation of a haematoma and inflammatory response",
            "Remodelling of bone to its original shape",
            "Formation of a hard bony callus",
            "Conversion of woven bone to lamellar bone"
        ],
        "answer_index": 0,
        "explanation": (
            "The first stage of fracture healing is formation of a blood clot (haematoma) and an inflammatory response, "
            "followed by soft callus, hard callus, and remodelling."
        ),
    },

    # =================
    # Joints & Muscle
    # =================
    {
        "id": 440,
        "topic": "Joints & Muscle",
        "question": "Articular cartilage in synovial joints is composed of:",
        "options": [
            "Hyaline cartilage without perichondrium",
            "Elastic cartilage with perichondrium",
            "Fibrocartilage only",
            "Dense regular connective tissue"
        ],
        "answer_index": 0,
        "explanation": (
            "Articular cartilage is hyaline cartilage that lacks a perichondrium; it covers the ends of bones in synovial joints."
        ),
    },
    {
        "id": 441,
        "topic": "Joints & Muscle",
        "question": "Which structure helps reduce friction between skin and underlying bone at a joint?",
        "options": [
            "Subcutaneous bursa",
            "Synovial membrane only",
            "Meniscus",
            "Articular cartilage"
        ],
        "answer_index": 0,
        "explanation": (
            "A bursa is a fluid-filled sac that reduces friction between moving structures such as skin and bone or tendon and bone."
        ),
    },
    {
        "id": 442,
        "topic": "Joints & Muscle",
        "question": "Cardiac muscle cells are characterised by:",
        "options": [
            "Branched fibres with intercalated discs",
            "Long, unbranched, multinucleated fibres with no intercalated discs",
            "Non-striated cells with no cross striations",
            "Voluntary control via somatic motor neurons"
        ],
        "answer_index": 0,
        "explanation": (
            "Cardiac muscle fibres are striated, branched, and connected by intercalated discs, and they contract involuntarily."
        ),
    },
    {
        "id": 443,
        "topic": "Joints & Muscle",
        "question": "Which of the following is characteristic of smooth muscle?",
        "options": [
            "Non-striated, spindle-shaped cells with a single central nucleus",
            "Striated cells with multiple peripheral nuclei",
            "Branched fibres with intercalated discs",
            "Cells arranged into sarcomeres with Z-lines"
        ],
        "answer_index": 0,
        "explanation": (
            "Smooth muscle cells are spindle-shaped, non-striated, with a single central nucleus, and are found in the walls of hollow organs."
        ),
    },
    {
        "id": 444,
        "topic": "Joints & Muscle",
        "question": "Muscle tone refers to:",
        "options": [
            "A state of partial contraction in resting muscle",
            "A maximal voluntary contraction",
            "Complete flaccid paralysis",
            "Permanent shortening of a muscle"
        ],
        "answer_index": 0,
        "explanation": (
            "Muscle tone is the slight, continuous contraction of muscle at rest, maintained by reflex activity, not a full contraction."
        ),
    },

    # ====================================
    # Nervous System (CNS & PNS general)
    # ====================================
    {
        "id": 450,
        "topic": "Nervous System (CNS & PNS)",
        "question": "The dorsal root ganglion contains cell bodies of:",
        "options": [
            "Sensory (afferent) neurons",
            "Motor (efferent) neurons",
            "Preganglionic sympathetic neurons",
            "Interneurons"
        ],
        "answer_index": 0,
        "explanation": (
            "Dorsal root ganglia contain the cell bodies of primary sensory neurons whose peripheral processes carry information from receptors."
        ),
    },
    {
        "id": 451,
        "topic": "Nervous System (CNS & PNS)",
        "question": "The cerebellum is primarily concerned with:",
        "options": [
            "Coordination of movement and balance",
            "Conscious perception of sensation",
            "Initiation of voluntary movement",
            "Production of cerebrospinal fluid"
        ],
        "answer_index": 0,
        "explanation": (
            "The cerebellum fine-tunes and coordinates movement, posture, and balance but does not initiate movement."
        ),
    },
    {
        "id": 452,
        "topic": "Nervous System (CNS & PNS)",
        "question": "Which lobe of the cerebral hemisphere contains the primary motor cortex?",
        "options": [
            "Frontal lobe",
            "Parietal lobe",
            "Temporal lobe",
            "Occipital lobe"
        ],
        "answer_index": 0,
        "explanation": (
            "The primary motor cortex is located in the precentral gyrus of the frontal lobe."
        ),
    },
    {
        "id": 453,
        "topic": "Nervous System (CNS & PNS)",
        "question": "Projection fibres in the brain connect:",
        "options": [
            "The cerebral cortex with lower brain centres and the spinal cord",
            "Areas within the same hemisphere only",
            "The two hemispheres only",
            "The cerebellum with the spinal cord only"
        ],
        "answer_index": 0,
        "explanation": (
            "Projection fibres run between the cerebral cortex and lower brain or spinal cord centres (e.g. internal capsule)."
        ),
    },
    {
        "id": 454,
        "topic": "Nervous System (CNS & PNS)",
        "question": "Myelinated nerve fibres conduct impulses:",
        "options": [
            "By saltatory conduction from node to node",
            "Only in one direction due to the myelin",
            "More slowly than unmyelinated fibres",
            "Only in the central nervous system"
        ],
        "answer_index": 0,
        "explanation": (
            "Myelinated fibres conduct impulses by saltatory conduction, jumping from node of Ranvier to node, which is faster than conduction in unmyelinated fibres."
        ),
    },

    # ==========
    # ANS
    # ==========
    {
        "id": 460,
        "topic": "ANS",
        "question": "Parasympathetic postganglionic fibres typically release:",
        "options": [
            "Acetylcholine",
            "Noradrenaline",
            "Dopamine",
            "Serotonin"
        ],
        "answer_index": 0,
        "explanation": (
            "Most parasympathetic postganglionic fibres release acetylcholine at their effector organs."
        ),
    },
    {
        "id": 461,
        "topic": "ANS",
        "question": "Which structure receives only sympathetic innervation (no direct parasympathetic supply)?",
        "options": [
            "Adrenal medulla",
            "Heart",
            "Bronchial smooth muscle",
            "Salivary glands"
        ],
        "answer_index": 0,
        "explanation": (
            "The adrenal medulla is innervated by preganglionic sympathetic fibres and releases adrenaline and noradrenaline into the blood."
        ),
    },
    {
        "id": 462,
        "topic": "ANS",
        "question": "Which receptor type is typically found at the neuromuscular junction of skeletal muscle?",
        "options": [
            "Nicotinic cholinergic receptors",
            "Muscarinic cholinergic receptors",
            "Alpha-adrenergic receptors",
            "Beta-adrenergic receptors"
        ],
        "answer_index": 0,
        "explanation": (
            "Nicotinic cholinergic receptors are present at the neuromuscular junction, while muscarinic receptors are on parasympathetic effector organs."
        ),
    },
    {
        "id": 463,
        "topic": "ANS",
        "question": "A typical effect of sympathetic stimulation on the gastrointestinal tract is:",
        "options": [
            "Decreased motility and secretion",
            "Increased motility and secretion",
            "Relaxation of sphincters",
            "Stimulation of peristalsis"
        ],
        "answer_index": 0,
        "explanation": (
            "Sympathetic activity generally inhibits GI activity by reducing motility and secretions and constricting sphincters."
        ),
    },
    {
        "id": 464,
        "topic": "ANS",
        "question": "Parasympathetic ganglia are usually located:",
        "options": [
            "Near or within the walls of target organs",
            "In a chain alongside the vertebral column",
            "In the dorsal root ganglia",
            "In the adrenal cortex"
        ],
        "answer_index": 0,
        "explanation": (
            "Parasympathetic ganglia tend to be close to or within the target organ, whereas sympathetic chain ganglia lie alongside the vertebral column."
        ),
    },

    # ===========================
    # Heart & Blood Vessels
    # ===========================
    {
        "id": 470,
        "topic": "Heart & Blood Vessels",
        "question": "The left coronary artery typically divides into:",
        "options": [
            "Anterior interventricular (LAD) and circumflex branches",
            "Marginal and posterior interventricular branches",
            "Right marginal and nodal branches",
            "Only a single continuous trunk"
        ],
        "answer_index": 0,
        "explanation": (
            "The left coronary artery usually divides into the anterior interventricular (LAD) and circumflex branches shortly after its origin."
        ),
    },
    {
        "id": 471,
        "topic": "Heart & Blood Vessels",
        "question": "The pulmonary trunk carries blood from:",
        "options": [
            "Right ventricle to the lungs",
            "Left ventricle to the body",
            "Right atrium to the right ventricle",
            "Left atrium to the left ventricle"
        ],
        "answer_index": 0,
        "explanation": (
            "The pulmonary trunk arises from the right ventricle and carries deoxygenated blood to the lungs via the pulmonary arteries."
        ),
    },
    {
        "id": 472,
        "topic": "Heart & Blood Vessels",
        "question": "Coronary sinus drains blood directly into the:",
        "options": [
            "Right atrium",
            "Left atrium",
            "Right ventricle",
            "Left ventricle"
        ],
        "answer_index": 0,
        "explanation": (
            "The coronary sinus collects most of the venous blood from the heart and opens into the right atrium."
        ),
    },
    {
        "id": 473,
        "topic": "Heart & Blood Vessels",
        "question": "Capillaries are best described as:",
        "options": [
            "Thin-walled vessels made of endothelium and a basal lamina",
            "Thick-walled vessels with multiple elastic lamellae",
            "Vessels with valves to prevent backflow",
            "Vessels with three distinct tunics and no exchange function"
        ],
        "answer_index": 0,
        "explanation": (
            "Capillaries consist mainly of a single layer of endothelial cells and a basal lamina, facilitating exchange between blood and tissues."
        ),
    },
    {
        "id": 474,
        "topic": "Heart & Blood Vessels",
        "question": "Which vessel carries oxygenated blood from the lungs to the heart?",
        "options": [
            "Pulmonary veins",
            "Pulmonary arteries",
            "Superior vena cava",
            "Azygos vein"
        ],
        "answer_index": 0,
        "explanation": (
            "Pulmonary veins carry oxygenated blood from the lungs to the left atrium."
        ),
    },
]

MORE_QUESTIONS = [
    # =========================
    # Anatomical Terms & Planes
    # =========================
    {
        "id": 500,
        "topic": "Anatomical Terms & Planes",
        "question": "Which term describes movement of the sole of the foot so that it faces medially?",
        "options": [
            "Inversion",
            "Eversion",
            "Dorsiflexion",
            "Plantarflexion"
        ],
        "answer_index": 0,
        "explanation": (
            "Inversion turns the sole of the foot medially. Eversion turns it laterally. "
            "Dorsiflexion brings the dorsum of the foot towards the shin; plantarflexion points the toes downwards."
        ),
    },
    {
        "id": 501,
        "topic": "Anatomical Terms & Planes",
        "question": "The dorsal surface of the foot refers to:",
        "options": [
            "The superior surface facing upwards in anatomical position",
            "The plantar surface in contact with the ground",
            "The medial border of the foot",
            "The lateral border of the foot"
        ],
        "answer_index": 0,
        "explanation": (
            "The dorsal surface of the foot is the superior surface. The plantar surface is the inferior, weight-bearing surface."
        ),
    },
    {
        "id": 502,
        "topic": "Anatomical Terms & Planes",
        "question": "The axial skeleton includes which of the following?",
        "options": [
            "Skull, vertebral column, ribs, and sternum",
            "Upper and lower limb bones",
            "Pectoral and pelvic girdles only",
            "Clavicle and scapula only"
        ],
        "answer_index": 0,
        "explanation": (
            "The axial skeleton consists of the skull, vertebral column, ribs, and sternum. "
            "The appendicular skeleton includes limb bones and their girdles."
        ),
    },
    {
        "id": 503,
        "topic": "Anatomical Terms & Planes",
        "question": "Flexion at the ankle joint that brings the dorsum of the foot towards the leg is called:",
        "options": [
            "Dorsiflexion",
            "Plantarflexion",
            "Inversion",
            "Eversion"
        ],
        "answer_index": 0,
        "explanation": (
            "Dorsiflexion decreases the angle between the dorsum of the foot and the anterior leg. "
            "Plantarflexion increases it, pointing the toes downwards."
        ),
    },
    {
        "id": 504,
        "topic": "Anatomical Terms & Planes",
        "question": "Which option correctly pairs body cavity and main contents?",
        "options": [
            "Thoracic cavity – lungs and heart",
            "Abdominal cavity – brain and spinal cord",
            "Cranial cavity – lungs and mediastinum",
            "Pelvic cavity – liver and pancreas"
        ],
        "answer_index": 0,
        "explanation": (
            "The thoracic cavity contains the lungs and heart (within the mediastinum). "
            "The cranial cavity contains the brain; the vertebral canal contains the spinal cord."
        ),
    },

    # =================
    # Membrane Transport
    # =================
    {
        "id": 505,
        "topic": "Membrane Transport",
        "question": "Primary active transport is best defined as:",
        "options": [
            "Transport that directly uses ATP to move solutes against their gradient",
            "Transport that uses ion gradients generated by other pumps",
            "Passive movement of solutes down their gradient",
            "Movement of water only through aquaporins"
        ],
        "answer_index": 0,
        "explanation": (
            "Primary active transporters, such as Na⁺/K⁺-ATPase, use ATP directly at the pump to move solutes against their gradients."
        ),
    },
    {
        "id": 506,
        "topic": "Membrane Transport",
        "question": "Which of the following is an antiporter?",
        "options": [
            "Na⁺/Ca²⁺ exchanger",
            "Na⁺–glucose cotransporter",
            "Aquaporin",
            "Voltage-gated Na⁺ channel"
        ],
        "answer_index": 0,
        "explanation": (
            "The Na⁺/Ca²⁺ exchanger moves Na⁺ and Ca²⁺ in opposite directions across the membrane and is an antiporter."
        ),
    },
    {
        "id": 507,
        "topic": "Membrane Transport",
        "question": "Receptor-mediated endocytosis is characterised by:",
        "options": [
            "Selective uptake of specific ligands via clathrin-coated pits",
            "Non-specific uptake of extracellular fluid only",
            "Exocytosis of vesicles",
            "Passive diffusion through lipid bilayer"
        ],
        "answer_index": 0,
        "explanation": (
            "Receptor-mediated endocytosis uses specific receptors and clathrin-coated pits to internalise selected ligands, "
            "e.g. LDL uptake."
        ),
    },
    {
        "id": 508,
        "topic": "Membrane Transport",
        "question": "Channel proteins differ from carrier proteins in that channels:",
        "options": [
            "Form continuous pores for rapid ion flow when open",
            "Bind solutes and undergo conformational cycling for each transport event",
            "Are always saturable at low concentrations",
            "Transport solutes only against gradients"
        ],
        "answer_index": 0,
        "explanation": (
            "Ion channels provide a water-filled pore that can open or close, allowing rapid passive diffusion. "
            "Carriers bind solutes and change conformation with each cycle and therefore have lower maximal rates."
        ),
    },
    {
        "id": 509,
        "topic": "Membrane Transport",
        "question": "Which condition would most increase the rate of diffusion of a lipid-soluble drug across a membrane?",
        "options": [
            "Increased concentration gradient and high lipid solubility",
            "Decreased temperature and decreased surface area",
            "Increased membrane thickness",
            "Lower concentration gradient with low permeability"
        ],
        "answer_index": 0,
        "explanation": (
            "By Fick’s law, diffusion rate increases with larger concentration gradient, greater surface area, higher permeability, "
            "and decreases with greater thickness."
        ),
    },

    # =====================
    # Epithelium & Glands
    # =====================
    {
        "id": 510,
        "topic": "Epithelium & Glands",
        "question": "The basement membrane is mainly composed of:",
        "options": [
            "Basal lamina and reticular lamina",
            "Keratin and desmosomes",
            "Elastic cartilage and collagen type I",
            "Fibroblasts and adipocytes"
        ],
        "answer_index": 0,
        "explanation": (
            "The basement membrane has a basal lamina (from epithelium) and a reticular lamina (from underlying connective tissue). "
            "It supports and anchors the epithelium."
        ),
    },
    {
        "id": 511,
        "topic": "Epithelium & Glands",
        "question": "In chronic smoking, the respiratory epithelium of the trachea may undergo:",
        "options": [
            "Metaplasia from pseudostratified ciliated columnar to stratified squamous epithelium",
            "Hypertrophy of goblet cells only",
            "Necrosis followed by cartilage formation",
            "Replacement by simple squamous epithelium for gas exchange"
        ],
        "answer_index": 0,
        "explanation": (
            "Smoking can cause metaplasia, where ciliated columnar epithelium is replaced by stratified squamous epithelium, "
            "reducing mucociliary clearance."
        ),
    },
    {
        "id": 512,
        "topic": "Epithelium & Glands",
        "question": "Microvilli on epithelial cells function mainly to:",
        "options": [
            "Increase surface area for absorption",
            "Propel mucus along the surface",
            "Form tight junctions",
            "Anchor the epithelium to the basement membrane"
        ],
        "answer_index": 0,
        "explanation": (
            "Microvilli, especially in the small intestine and kidney, greatly increase apical surface area to enhance absorption. "
            "Cilia, not microvilli, move mucus."
        ),
    },
    {
        "id": 513,
        "topic": "Epithelium & Glands",
        "question": "Serous acini in salivary glands secrete:",
        "options": [
            "Watery, enzyme-rich fluid",
            "Thick, mucous secretion only",
            "Sebum rich in lipids",
            "Hormones directly into blood"
        ],
        "answer_index": 0,
        "explanation": (
            "Serous cells secrete watery, enzyme-rich fluid (e.g. amylase), while mucous cells secrete viscous mucus."
        ),
    },
    {
        "id": 514,
        "topic": "Epithelium & Glands",
        "question": "Tight junctions (zonulae occludentes) between epithelial cells:",
        "options": [
            "Form a seal regulating paracellular passage of substances",
            "Anchor intermediate filaments to the basement membrane",
            "Allow rapid communication via connexons",
            "Provide contractile force for microvilli movement"
        ],
        "answer_index": 0,
        "explanation": (
            "Tight junctions seal neighbouring cells near the apical border, controlling paracellular permeability and maintaining polarity."
        ),
    },

    # =====================================
    # Connective Tissue, Cartilage & Bone
    # =====================================
    {
        "id": 515,
        "topic": "Connective Tissue, Cartilage & Bone",
        "question": "Mast cells in connective tissue are best known for releasing:",
        "options": [
            "Histamine and heparin during inflammatory responses",
            "Antibodies into the bloodstream",
            "Collagen type I fibres",
            "Surfactant into alveoli"
        ],
        "answer_index": 0,
        "explanation": (
            "Mast cells contain granules with histamine, heparin, and other mediators released during allergic and inflammatory reactions."
        ),
    },
    {
        "id": 516,
        "topic": "Connective Tissue, Cartilage & Bone",
        "question": "White adipose tissue functions mainly to:",
        "options": [
            "Store energy as triglycerides and provide insulation",
            "Produce bone matrix directly",
            "Form the reticular stroma of lymphoid organs",
            "Generate heat in newborns as its primary function"
        ],
        "answer_index": 0,
        "explanation": (
            "White adipose tissue stores energy, cushions organs, and insulates. Brown fat is specialised for heat production, especially in neonates."
        ),
    },
    {
        "id": 517,
        "topic": "Connective Tissue, Cartilage & Bone",
        "question": "The perichondrium:",
        "options": [
            "Surrounds most hyaline cartilage and contains cells that can generate new cartilage",
            "Lines the medullary cavity of long bones",
            "Is absent in elastic cartilage",
            "Is present over articular cartilage surfaces"
        ],
        "answer_index": 0,
        "explanation": (
            "Perichondrium is a connective tissue sheath around most hyaline and elastic cartilage (not articular cartilage), "
            "containing chondrogenic cells for appositional growth."
        ),
    },
    {
        "id": 518,
        "topic": "Connective Tissue, Cartilage & Bone",
        "question": "Woven bone differs from lamellar bone because woven bone:",
        "options": [
            "Has randomly arranged collagen fibres and is formed rapidly",
            "Is always found in healthy adult skeleton only",
            "Is more mechanically strong than lamellar bone",
            "Lacks osteocytes"
        ],
        "answer_index": 0,
        "explanation": (
            "Woven bone is produced quickly (e.g. in fracture repair or fetal bone), with irregular collagen orientation. "
            "It is later remodelled into stronger lamellar bone."
        ),
    },
    {
        "id": 519,
        "topic": "Connective Tissue, Cartilage & Bone",
        "question": "Osteoid refers to:",
        "options": [
            "Unmineralised organic bone matrix produced by osteoblasts",
            "Fully mineralised bone matrix",
            "Cartilage matrix prior to ossification",
            "Bone marrow stroma only"
        ],
        "answer_index": 0,
        "explanation": (
            "Osteoid is the organic component of bone matrix (mainly type I collagen and ground substance) before mineralisation with calcium salts."
        ),
    },

    # =================
    # Joints & Muscle
    # =================
    {
        "id": 520,
        "topic": "Joints & Muscle",
        "question": "A ball-and-socket joint, such as the shoulder, allows:",
        "options": [
            "Multiaxial movement including flexion, extension, abduction, adduction, rotation, and circumduction",
            "Only flexion and extension",
            "Only rotation around one axis",
            "No movement"
        ],
        "answer_index": 0,
        "explanation": (
            "Ball-and-socket joints are multiaxial and permit the greatest range of motion, including circumduction and rotation."
        ),
    },
    {
        "id": 521,
        "topic": "Joints & Muscle",
        "question": "Which of the following is an example of a plane (gliding) synovial joint?",
        "options": [
            "Zygapophyseal joints between vertebral articular processes",
            "Elbow joint",
            "Hip joint",
            "First carpometacarpal joint of the thumb"
        ],
        "answer_index": 0,
        "explanation": (
            "Zygapophyseal joints and many intercarpal joints are plane joints that permit sliding or gliding movements."
        ),
    },
    {
        "id": 522,
        "topic": "Joints & Muscle",
        "question": "In muscle terminology, the term 'origin' usually refers to:",
        "options": [
            "The more fixed, proximal attachment of the muscle",
            "The more mobile, distal attachment",
            "Any attachment on a bone",
            "The tendon closest to the skin"
        ],
        "answer_index": 0,
        "explanation": (
            "The origin is typically the proximal, less moveable attachment; the insertion is the distal, more moveable attachment."
        ),
    },
    {
        "id": 523,
        "topic": "Joints & Muscle",
        "question": "Isometric contraction occurs when:",
        "options": [
            "Muscle tension increases but length does not change",
            "Muscle shortens while generating constant tension",
            "Muscle lengthens under load only",
            "There is no electrical activity in the muscle"
        ],
        "answer_index": 0,
        "explanation": (
            "In isometric contraction, the muscle develops tension without changing length (e.g. holding a weight still). "
            "Isotonic contractions change length."
        ),
    },
    {
        "id": 524,
        "topic": "Joints & Muscle",
        "question": "At the neuromuscular junction, acetylcholine binds to receptors located on the:",
        "options": [
            "Motor endplate of the skeletal muscle fibre",
            "Presynaptic terminal of the motor neuron",
            "Myelin sheath",
            "Sarcomere Z line"
        ],
        "answer_index": 0,
        "explanation": (
            "ACh is released from the motor neuron terminal and binds to nicotinic receptors on the motor endplate membrane of the muscle fibre."
        ),
    },

    # ====================================
    # Nervous System (CNS & PNS)
    # ====================================
    {
        "id": 525,
        "topic": "Nervous System (CNS & PNS)",
        "question": "Broca’s area, important for motor speech, is located in:",
        "options": [
            "The inferior frontal gyrus of the dominant hemisphere",
            "The superior temporal gyrus bilaterally",
            "The occipital lobe",
            "The cerebellar hemispheres"
        ],
        "answer_index": 0,
        "explanation": (
            "Broca’s area lies in the dominant (usually left) inferior frontal gyrus and is essential for the motor aspect of speech production."
        ),
    },
    {
        "id": 526,
        "topic": "Nervous System (CNS & PNS)",
        "question": "The cervical and lumbosacral enlargements of the spinal cord correspond to:",
        "options": [
            "Regions giving rise to nerves of the upper and lower limbs",
            "Areas of CSF production",
            "Origins of cranial nerves",
            "Sites of sympathetic outflow only"
        ],
        "answer_index": 0,
        "explanation": (
            "These enlargements contain additional neurons for plexuses supplying upper (brachial) and lower (lumbosacral) limbs."
        ),
    },
    {
        "id": 527,
        "topic": "Nervous System (CNS & PNS)",
        "question": "Cerebrospinal fluid (CSF) is mainly produced by:",
        "options": [
            "Choroid plexuses within the ventricles",
            "Dura mater",
            "Ependymal cells lining the central canal only",
            "Venous sinuses"
        ],
        "answer_index": 0,
        "explanation": (
            "CSF is produced by specialised ependymal cells in the choroid plexuses of the ventricles, then circulates and is reabsorbed into venous sinuses."
        ),
    },
    {
        "id": 528,
        "topic": "Nervous System (CNS & PNS)",
        "question": "The blood–brain barrier is primarily formed by:",
        "options": [
            "Tight junctions between capillary endothelial cells and astrocyte end-feet",
            "Fenestrated capillaries with large pores",
            "Loose junctions between arachnoid cells",
            "Open channels between neurons"
        ],
        "answer_index": 0,
        "explanation": (
            "The BBB is maintained by tight junctions of CNS capillary endothelium and astrocytic processes, restricting passage of many substances."
        ),
    },
    {
        "id": 529,
        "topic": "Nervous System (CNS & PNS)",
        "question": "A dermatome is best defined as:",
        "options": [
            "An area of skin supplied by a single spinal nerve",
            "A group of muscles supplied by a single nerve",
            "A segment of the spinal cord",
            "A region of cortex representing the skin"
        ],
        "answer_index": 0,
        "explanation": (
            "A dermatome is a skin area innervated by sensory fibres of one spinal nerve/root, useful clinically in localising lesions."
        ),
    },

    # ==========
    # ANS
    # ==========
    {
        "id": 530,
        "topic": "ANS",
        "question": "Stimulation of β₁-adrenergic receptors in the heart typically causes:",
        "options": [
            "Increased heart rate and contractility",
            "Decreased heart rate and contractility",
            "Bronchoconstriction",
            "Pupillary constriction"
        ],
        "answer_index": 0,
        "explanation": (
            "β₁-receptor activation in the heart increases rate and force of contraction (positive chronotropic and inotropic effects)."
        ),
    },
    {
        "id": 531,
        "topic": "ANS",
        "question": "Stimulation of β₂-adrenergic receptors in bronchial smooth muscle results in:",
        "options": [
            "Bronchodilation",
            "Bronchoconstriction",
            "Increased mucus secretion only",
            "No change in airway calibre"
        ],
        "answer_index": 0,
        "explanation": (
            "β₂-receptor activation relaxes bronchial smooth muscle, causing bronchodilation, important in asthma therapy."
        ),
    },
    {
        "id": 532,
        "topic": "ANS",
        "question": "White rami communicantes carry:",
        "options": [
            "Preganglionic sympathetic fibres from spinal nerve to sympathetic chain",
            "Postganglionic sympathetic fibres back to spinal nerve",
            "Parasympathetic fibres from the vagus nerve",
            "Sensory fibres only"
        ],
        "answer_index": 0,
        "explanation": (
            "White rami communicantes contain myelinated preganglionic sympathetic axons from spinal nerves T1–L2 to the sympathetic chain."
        ),
    },
    {
        "id": 533,
        "topic": "ANS",
        "question": "Nicotinic receptors in autonomic ganglia are located on:",
        "options": [
            "Postganglionic neuron cell bodies",
            "Effector organs",
            "Preganglionic terminals",
            "Skeletal muscle fibres only"
        ],
        "answer_index": 0,
        "explanation": (
            "Nicotinic receptors (Nn) on postganglionic neuron cell bodies in autonomic ganglia respond to ACh released from preganglionic fibres."
        ),
    },
    {
        "id": 534,
        "topic": "ANS",
        "question": "A classic parasympathetic effect on the eye is:",
        "options": [
            "Pupillary constriction (miosis) and accommodation for near vision",
            "Pupillary dilation and loss of accommodation",
            "Lid retraction",
            "Complete paralysis of extraocular muscles"
        ],
        "answer_index": 0,
        "explanation": (
            "Parasympathetic fibres via the oculomotor nerve constrict the pupil and contract ciliary muscle for near vision."
        ),
    },

    # ===========================
    # Heart & Blood Vessels
    # ===========================
    {
        "id": 535,
        "topic": "Heart & Blood Vessels",
        "question": "Arrange the normal cardiac conduction pathway in order:",
        "options": [
            "SA node → AV node → AV bundle → bundle branches → Purkinje fibres",
            "AV node → SA node → bundle branches → AV bundle → Purkinje fibres",
            "SA node → bundle branches → AV node → Purkinje fibres → AV bundle",
            "Purkinje fibres → SA node → AV node → AV bundle → bundle branches"
        ],
        "answer_index": 0,
        "explanation": (
            "The impulse originates in the SA node, spreads to AV node, then via AV bundle, bundle branches, and Purkinje fibres."
        ),
    },
    {
        "id": 536,
        "topic": "Heart & Blood Vessels",
        "question": "The fibrous pericardium functions mainly to:",
        "options": [
            "Anchor the heart and prevent over-distension",
            "Produce pericardial fluid",
            "Generate action potentials",
            "Store blood like a reservoir"
        ],
        "answer_index": 0,
        "explanation": (
            "The tough fibrous pericardium anchors the heart to surrounding structures and limits acute over-filling."
        ),
    },
    {
        "id": 537,
        "topic": "Heart & Blood Vessels",
        "question": "The tunica intima of a typical muscular artery contains:",
        "options": [
            "Endothelium, subendothelial connective tissue, and internal elastic lamina",
            "Smooth muscle bundles only",
            "External elastic lamina only",
            "Dense collagen with vasa vasorum"
        ],
        "answer_index": 0,
        "explanation": (
            "Tunica intima comprises the endothelial lining, a thin subendothelial layer, and an internal elastic lamina in many arteries."
        ),
    },
    {
        "id": 538,
        "topic": "Heart & Blood Vessels",
        "question": "Compared with large arteries, large veins typically have:",
        "options": [
            "Thinner walls and a relatively thicker tunica adventitia",
            "Thicker tunica media with more elastic lamellae",
            "No endothelium",
            "Higher blood pressure and faster flow"
        ],
        "answer_index": 0,
        "explanation": (
            "Large veins have thinner media but a thick adventitia, and often valves, with lower pressure and slower flow."
        ),
    },
    {
        "id": 539,
        "topic": "Heart & Blood Vessels",
        "question": "A portal vein is defined as a vein that:",
        "options": [
            "Connects two capillary beds in series",
            "Carries only oxygenated blood",
            "Drains directly into the right atrium",
            "Supplies the myocardium"
        ],
        "answer_index": 0,
        "explanation": (
            "Portal veins, such as the hepatic portal vein, connect one capillary bed (gut) to another (liver) before reaching the heart."
        ),
    },

    # =====================
    # Lymphatic System
    # =====================
    {
        "id": 540,
        "topic": "Lymphatic System",
        "question": "Lymph nodes receive lymph via:",
        "options": [
            "Multiple afferent vessels entering the convex surface",
            "A single afferent vessel at the hilum",
            "Only efferent vessels",
            "Direct arterial branches only"
        ],
        "answer_index": 0,
        "explanation": (
            "Several afferent lymphatic vessels enter on the convex surface; one efferent vessel leaves at the hilum."
        ),
    },
    {
        "id": 541,
        "topic": "Lymphatic System",
        "question": "In a typical lymph node, B-cell–rich lymphoid follicles are located mainly in the:",
        "options": [
            "Outer cortex",
            "Paracortex",
            "Medullary cords",
            "Hilum only"
        ],
        "answer_index": 0,
        "explanation": (
            "B-cell follicles lie in the outer cortex; the paracortex is T-cell rich; medullary cords contain plasma cells and macrophages."
        ),
    },
    {
        "id": 542,
        "topic": "Lymphatic System",
        "question": "The thymus is unique among lymphoid organs because:",
        "options": [
            "It has no afferent lymphatic vessels and is the site of T-cell maturation",
            "It filters lymph from peripheral tissues",
            "It stores mature B cells only",
            "It remains the same size throughout life"
        ],
        "answer_index": 0,
        "explanation": (
            "The thymus lacks afferent lymphatics, is a primary lymphoid organ for T-cell maturation, and undergoes involution after puberty."
        ),
    },
    {
        "id": 543,
        "topic": "Lymphatic System",
        "question": "Red pulp of the spleen is mainly involved in:",
        "options": [
            "Filtration and removal of old red blood cells",
            "Production of T lymphocytes",
            "Maturation of B cells only",
            "Production of surfactant"
        ],
        "answer_index": 0,
        "explanation": (
            "Red pulp contains splenic cords and sinusoids that filter blood and remove old or damaged erythrocytes."
        ),
    },
    {
        "id": 544,
        "topic": "Lymphatic System",
        "question": "Lacteals are:",
        "options": [
            "Lymphatic capillaries in intestinal villi that absorb dietary lipids",
            "Venous sinuses in the liver",
            "Capillaries in the renal cortex",
            "Glands in the dermis"
        ],
        "answer_index": 0,
        "explanation": (
            "Lacteals are specialised lymphatic capillaries in small intestinal villi that take up chylomicrons (lipids)."
        ),
    },

    # =====================
    # Respiratory System
    # =====================
    {
        "id": 545,
        "topic": "Respiratory System",
        "question": "The boundary between upper and lower respiratory tracts is usually taken as the level of the:",
        "options": [
            "Lower border of the cricoid cartilage",
            "Soft palate",
            "Carina",
            "Alveolar ducts"
        ],
        "answer_index": 0,
        "explanation": (
            "Clinically, the upper tract includes nose to larynx; the lower tract begins at the trachea, whose upper limit is at the cricoid cartilage."
        ),
    },
    {
        "id": 546,
        "topic": "Respiratory System",
        "question": "Which laryngeal cartilage forms a complete ring around the airway?",
        "options": [
            "Cricoid cartilage",
            "Thyroid cartilage",
            "Arytenoid cartilage",
            "Epiglottis"
        ],
        "answer_index": 0,
        "explanation": (
            "The cricoid is the only complete ring of cartilage in the airway and lies below the thyroid cartilage."
        ),
    },
    {
        "id": 547,
        "topic": "Respiratory System",
        "question": "Quiet expiration at rest is mainly:",
        "options": [
            "A passive process due to elastic recoil of lungs and chest wall",
            "An active process involving abdominal muscles only",
            "Driven by contraction of the diaphragm",
            "Produced by contraction of internal intercostals in all breaths"
        ],
        "answer_index": 0,
        "explanation": (
            "Quiet expiration is passive, relying on elastic recoil. Active expiration recruits internal intercostals and abdominal muscles."
        ),
    },
    {
        "id": 548,
        "topic": "Respiratory System",
        "question": "The bronchial circulation supplies:",
        "options": [
            "Oxygenated blood to lung tissue (bronchi and connective tissue)",
            "Deoxygenated blood to the alveoli",
            "All of the pulmonary capillaries",
            "Only the visceral pleura"
        ],
        "answer_index": 0,
        "explanation": (
            "Bronchial arteries (from systemic circulation) provide oxygenated blood to the conducting airways and supporting tissues."
        ),
    },
    {
        "id": 549,
        "topic": "Respiratory System",
        "question": "Ventilation–perfusion (V/Q) matching is important because it:",
        "options": [
            "Ensures adequate gas exchange by matching airflow to blood flow",
            "Only determines lung volumes",
            "Controls heart rate directly",
            "Has no effect on oxygenation"
        ],
        "answer_index": 0,
        "explanation": (
            "Optimal gas exchange requires appropriate matching of ventilation (airflow) to perfusion (blood flow) in different lung regions."
        ),
    },

    # =================
    # Urinary System
    # =================
    {
        "id": 550,
        "topic": "Urinary System",
        "question": "The juxtaglomerular apparatus includes all of the following EXCEPT:",
        "options": [
            "Cells of the proximal convoluted tubule",
            "Macula densa cells of the distal tubule",
            "Juxtaglomerular (granular) cells of the afferent arteriole",
            "Extraglomerular mesangial cells"
        ],
        "answer_index": 0,
        "explanation": (
            "The JGA is formed by macula densa, juxtaglomerular cells, and extraglomerular mesangial cells. "
            "Proximal tubule cells are not part of it."
        ),
    },
    {
        "id": 551,
        "topic": "Urinary System",
        "question": "Macula densa cells sense changes in:",
        "options": [
            "NaCl concentration in the distal tubule fluid",
            "Oxygen tension in the renal vein",
            "Glucose levels in the filtrate",
            "Potassium in the collecting duct only"
        ],
        "answer_index": 0,
        "explanation": (
            "Macula densa cells monitor NaCl concentration in the distal tubule and signal JG cells to adjust renin release and GFR."
        ),
    },
    {
        "id": 552,
        "topic": "Urinary System",
        "question": "The right kidney is usually located slightly lower than the left because of the presence of the:",
        "options": [
            "Liver",
            "Spleen",
            "Pancreas",
            "Stomach"
        ],
        "answer_index": 0,
        "explanation": (
            "The large right lobe of the liver pushes the right kidney slightly lower than the left."
        ),
    },
    {
        "id": 553,
        "topic": "Urinary System",
        "question": "The internal urethral sphincter in males is composed of:",
        "options": [
            "Smooth muscle under involuntary control",
            "Skeletal muscle under voluntary control",
            "Elastic cartilage",
            "Connective tissue only"
        ],
        "answer_index": 0,
        "explanation": (
            "The internal sphincter is smooth muscle at the bladder neck (involuntary); the external sphincter is skeletal muscle (voluntary)."
        ),
    },
    {
        "id": 554,
        "topic": "Urinary System",
        "question": "Aldosterone acts primarily on which part of the nephron?",
        "options": [
            "Distal convoluted tubule and collecting duct",
            "Glomerulus",
            "Proximal convoluted tubule only",
            "Thin descending limb of loop of Henle"
        ],
        "answer_index": 0,
        "explanation": (
            "Aldosterone increases Na⁺ reabsorption and K⁺ secretion mainly in the distal tubule and collecting duct."
        ),
    },

    # =================
    # Endocrine System
    # =================
    {
        "id": 555,
        "topic": "Endocrine System",
        "question": "Thyroid follicles are filled with:",
        "options": [
            "Colloid containing thyroglobulin",
            "Serous fluid only",
            "Synovial fluid",
            "Bile"
        ],
        "answer_index": 0,
        "explanation": (
            "Thyroid follicles contain colloid rich in thyroglobulin, the precursor for thyroid hormone synthesis."
        ),
    },
    {
        "id": 556,
        "topic": "Endocrine System",
        "question": "Which zone of the adrenal cortex primarily secretes aldosterone?",
        "options": [
            "Zona glomerulosa",
            "Zona fasciculata",
            "Zona reticularis",
            "Medulla"
        ],
        "answer_index": 0,
        "explanation": (
            "Zona glomerulosa secretes mineralocorticoids (mainly aldosterone). "
            "Zona fasciculata secretes glucocorticoids, and zona reticularis secretes androgens."
        ),
    },
    {
        "id": 557,
        "topic": "Endocrine System",
        "question": "TRH from the hypothalamus stimulates the anterior pituitary to release:",
        "options": [
            "TSH (and prolactin)",
            "ACTH only",
            "GH only",
            "FSH and LH only"
        ],
        "answer_index": 0,
        "explanation": (
            "Thyrotropin-releasing hormone (TRH) stimulates TSH release primarily, and also prolactin to a lesser extent."
        ),
    },
    {
        "id": 558,
        "topic": "Endocrine System",
        "question": "Steroid hormones typically act by:",
        "options": [
            "Binding intracellular receptors that regulate gene transcription",
            "Binding membrane receptors and activating second messengers only",
            "Opening ion channels directly like neurotransmitters",
            "Being stored in secretory granules before release"
        ],
        "answer_index": 0,
        "explanation": (
            "Steroid hormones are lipid-soluble, diffuse into cells, and bind intracellular receptors that modulate transcription."
        ),
    },
    {
        "id": 559,
        "topic": "Endocrine System",
        "question": "Negative feedback in endocrine systems means:",
        "options": [
            "Hormone output is reduced when its effects are sufficient",
            "Hormone always inhibits another hormone",
            "Hormone levels rise without regulation",
            "The system cannot respond to changes"
        ],
        "answer_index": 0,
        "explanation": (
            "In negative feedback, rising levels of a hormone or its effect reduce further secretion, maintaining homeostasis."
        ),
    },

    # ============================
    # Male Reproductive System
    # ============================
    {
        "id": 560,
        "topic": "Male Reproductive System",
        "question": "During normal development, the testes descend into the scrotum via the:",
        "options": [
            "Inguinal canal",
            "Obturator canal",
            "Femoral canal",
            "Pelvic inlet"
        ],
        "answer_index": 0,
        "explanation": (
            "The gubernaculum guides testicular descent through the inguinal canal into the scrotum."
        ),
    },
    {
        "id": 561,
        "topic": "Male Reproductive System",
        "question": "Spermatogenesis produces:",
        "options": [
            "Four haploid spermatozoa from each primary spermatocyte",
            "Two diploid spermatocytes from each spermatid",
            "Diploid spermatozoa identical to spermatogonia",
            "Haploid oocytes"
        ],
        "answer_index": 0,
        "explanation": (
            "Meiosis of one primary spermatocyte yields four haploid spermatids, which differentiate into spermatozoa."
        ),
    },
    {
        "id": 562,
        "topic": "Male Reproductive System",
        "question": "FSH in males primarily acts on:",
        "options": [
            "Sertoli cells to support spermatogenesis",
            "Leydig cells to stimulate testosterone secretion",
            "Epididymal cells to store sperm",
            "Prostatic cells to secrete PSA"
        ],
        "answer_index": 0,
        "explanation": (
            "FSH stimulates Sertoli cells, which support developing germ cells; LH stimulates Leydig cells to produce testosterone."
        ),
    },
    {
        "id": 563,
        "topic": "Male Reproductive System",
        "question": "Benign prostatic hyperplasia (BPH) most commonly affects which zone of the prostate?",
        "options": [
            "Transition zone around the proximal urethra",
            "Peripheral zone",
            "Central zone around ejaculatory ducts",
            "None; all zones equally"
        ],
        "answer_index": 0,
        "explanation": (
            "BPH arises mainly in the transition zone, leading to urethral compression and urinary symptoms."
        ),
    },
    {
        "id": 564,
        "topic": "Male Reproductive System",
        "question": "Which gland contributes a thin, milky, enzyme-rich secretion to semen?",
        "options": [
            "Prostate gland",
            "Seminal vesicle",
            "Bulbourethral gland",
            "Pituitary gland"
        ],
        "answer_index": 0,
        "explanation": (
            "The prostate secretes a thin, milky fluid containing enzymes like PSA; seminal vesicles provide fructose-rich fluid."
        ),
    },

    # ==============================
    # Female Reproductive System
    # ==============================
    {
        "id": 565,
        "topic": "Female Reproductive System",
        "question": "The ovarian follicle that has a large antrum and is close to ovulation is called a:",
        "options": [
            "Graafian (mature) follicle",
            "Primordial follicle",
            "Primary follicle",
            "Atretic follicle"
        ],
        "answer_index": 0,
        "explanation": (
            "A Graafian follicle has a large fluid-filled antrum and a cumulus oophorus surrounding the oocyte."
        ),
    },
    {
        "id": 566,
        "topic": "Female Reproductive System",
        "question": "The proliferative phase of the uterine cycle is driven mainly by:",
        "options": [
            "Oestrogen from developing follicles",
            "Progesterone from the corpus luteum",
            "FSH directly on the endometrium",
            "Prolactin from the pituitary"
        ],
        "answer_index": 0,
        "explanation": (
            "Rising oestrogen levels stimulate regeneration and proliferation of the endometrium after menstruation."
        ),
    },
    {
        "id": 567,
        "topic": "Female Reproductive System",
        "question": "Progesterone in the luteal phase mainly causes the endometrium to become:",
        "options": [
            "Secretory and suitable for implantation",
            "Thinner and atrophic",
            "Keratinised",
            "Replaced by fibrous tissue"
        ],
        "answer_index": 0,
        "explanation": (
            "Progesterone from the corpus luteum converts the proliferative endometrium into a secretory one ready for implantation."
        ),
    },
    {
        "id": 568,
        "topic": "Female Reproductive System",
        "question": "Cervical mucus around the time of ovulation becomes:",
        "options": [
            "Thin, watery, and more permeable to sperm",
            "Thick and impenetrable to sperm",
            "Completely absent",
            "Bloody in all cycles"
        ],
        "answer_index": 0,
        "explanation": (
            "Under oestrogen influence at mid-cycle, cervical mucus becomes thin and stretchy, facilitating sperm passage."
        ),
    },
    {
        "id": 569,
        "topic": "Female Reproductive System",
        "question": "The placenta performs all of the following functions EXCEPT:",
        "options": [
            "Producing maternal erythrocytes",
            "Gas exchange between mother and fetus",
            "Nutrient and waste exchange",
            "Hormone production (e.g. hCG, progesterone)"
        ],
        "answer_index": 0,
        "explanation": (
            "The placenta mediates exchange and produces hormones but does not produce maternal red blood cells."
        ),
    },

    # ====================================
    # Cell Division & Early Embryology
    # ====================================
    {
        "id": 570,
        "topic": "Cell Division & Early Embryology",
        "question": "Implantation of the blastocyst into the endometrium usually begins around:",
        "options": [
            "Day 6–7 after fertilisation",
            "Day 1 after fertilisation",
            "Day 14 after fertilisation",
            "Week 4 of gestation"
        ],
        "answer_index": 0,
        "explanation": (
            "The blastocyst typically begins to implant around day 6–7 after fertilisation in the receptive endometrium."
        ),
    },
    {
        "id": 571,
        "topic": "Cell Division & Early Embryology",
        "question": "Primary chorionic villi initially consist of:",
        "options": [
            "Cytotrophoblast covered by syncytiotrophoblast",
            "Mesoderm with fetal capillaries only",
            "Endodermal cells only",
            "Neural crest cells"
        ],
        "answer_index": 0,
        "explanation": (
            "Primary villi are formed by cytotrophoblast cores covered by syncytiotrophoblast; extraembryonic mesoderm later invades to form secondary and tertiary villi."
        ),
    },
    {
        "id": 572,
        "topic": "Cell Division & Early Embryology",
        "question": "The most critical period for major organogenesis in human development is:",
        "options": [
            "Weeks 3–8 of embryonic development",
            "First week only",
            "After 20 weeks of gestation",
            "The perinatal period"
        ],
        "answer_index": 0,
        "explanation": (
            "Organogenesis occurs mainly between weeks 3–8; teratogenic insults in this period can cause major congenital malformations."
        ),
    },
    {
        "id": 573,
        "topic": "Cell Division & Early Embryology",
        "question": "Ectoderm gives rise to all of the following EXCEPT:",
        "options": [
            "Skeletal muscles of the limbs",
            "Epidermis",
            "Central nervous system",
            "Peripheral nervous system (largely)"
        ],
        "answer_index": 0,
        "explanation": (
            "Skeletal muscle is derived from mesoderm. Ectoderm forms epidermis, CNS, PNS, and many neural crest derivatives."
        ),
    },
    {
        "id": 574,
        "topic": "Cell Division & Early Embryology",
        "question": "Neural crest cells contribute to the formation of:",
        "options": [
            "Melanocytes and components of the peripheral nervous system",
            "Hepatocytes",
            "Skeletal muscle of the limbs",
            "Endothelial cells of all blood vessels"
        ],
        "answer_index": 0,
        "explanation": (
            "Neural crest cells are pluripotent and give rise to melanocytes, many PNS structures, some craniofacial bones, parts of the heart outflow tract, and more."
        ),
    },
]

EVEN_MORE_QUESTIONS = [
    # =========================
    # Anatomical Terms & Planes
    # =========================
    {
        "id": 600,
        "topic": "Anatomical Terms & Planes",
        "question": "Which term describes a structure located farther from the surface of the body?",
        "options": [
            "Deep",
            "Superficial",
            "Inferior",
            "Proximal"
        ],
        "answer_index": 0,
        "explanation": (
            "Deep means farther from the surface of the body, whereas superficial means closer to the surface."
        ),
    },
    {
        "id": 601,
        "topic": "Anatomical Terms & Planes",
        "question": "Circumduction at the shoulder joint is best described as:",
        "options": [
            "A combination of flexion, extension, abduction, and adduction",
            "Rotation around a single axis only",
            "Pure flexion and extension in the sagittal plane",
            "Movement only in the transverse plane"
        ],
        "answer_index": 0,
        "explanation": (
            "Circumduction is a circular movement that combines flexion, extension, abduction, and adduction at a joint."
        ),
    },
    {
        "id": 602,
        "topic": "Anatomical Terms & Planes",
        "question": "Which term describes structures found on opposite sides of the body?",
        "options": [
            "Contralateral",
            "Ipsilateral",
            "Bilateral",
            "Unilateral"
        ],
        "answer_index": 0,
        "explanation": (
            "Contralateral refers to structures on opposite sides; ipsilateral means on the same side."
        ),
    },
    {
        "id": 603,
        "topic": "Anatomical Terms & Planes",
        "question": "The term 'palmar' refers specifically to the:",
        "options": [
            "Anterior surface of the hand",
            "Posterior surface of the hand",
            "Sole of the foot",
            "Back of the leg"
        ],
        "answer_index": 0,
        "explanation": (
            "Palmar refers to the anterior surface of the hand; plantar refers to the sole of the foot."
        ),
    },
    {
        "id": 604,
        "topic": "Anatomical Terms & Planes",
        "question": "Which of these planes would best show both kidneys in one view on an imaging scan?",
        "options": [
            "Transverse (axial) plane",
            "Median plane",
            "Parasagittal plane through the right side",
            "Oblique plane through the left flank only"
        ],
        "answer_index": 0,
        "explanation": (
            "A transverse (axial) cut through the upper abdomen will show both kidneys in a single slice."
        ),
    },

    # =================
    # Membrane Transport
    # =================
    {
        "id": 605,
        "topic": "Membrane Transport",
        "question": "In a hypertonic extracellular solution, a typical cell will:",
        "options": [
            "Lose water and shrink",
            "Gain water and swell",
            "Remain exactly the same size",
            "Actively pump water into itself"
        ],
        "answer_index": 0,
        "explanation": (
            "In a hypertonic solution, water leaves the cell by osmosis, causing it to shrink (crenate)."
        ),
    },
    {
        "id": 606,
        "topic": "Membrane Transport",
        "question": "Which of the following is TRUE for both simple diffusion and facilitated diffusion?",
        "options": [
            "They move substances down their concentration gradient",
            "They require ATP directly",
            "They always use carrier proteins",
            "They can move substances against their gradient"
        ],
        "answer_index": 0,
        "explanation": (
            "Both are passive processes and move substances down their concentration gradient without direct ATP use."
        ),
    },
    {
        "id": 607,
        "topic": "Membrane Transport",
        "question": "Pinocytosis is best described as:",
        "options": [
            "Non-specific uptake of fluid and small molecules via vesicles",
            "Engulfment of large particles such as bacteria",
            "Exocytosis of neurotransmitters",
            "Channel-mediated transport of ions"
        ],
        "answer_index": 0,
        "explanation": (
            "Pinocytosis is 'cell drinking', taking in extracellular fluid and dissolved solutes via small vesicles."
        ),
    },
    {
        "id": 608,
        "topic": "Membrane Transport",
        "question": "Which condition will DECREASE the rate of diffusion across a membrane?",
        "options": [
            "Increased membrane thickness",
            "Increased temperature",
            "Increased surface area",
            "Higher permeability to the solute"
        ],
        "answer_index": 0,
        "explanation": (
            "Diffusion is slower when the membrane is thicker; greater surface area, temperature, and permeability increase diffusion."
        ),
    },
    {
        "id": 609,
        "topic": "Membrane Transport",
        "question": "The Gibbs–Donnan effect across a membrane is mainly due to:",
        "options": [
            "Presence of non-diffusible charged particles on one side of the membrane",
            "ATP hydrolysis at the membrane surface",
            "Opening of voltage-gated Na⁺ channels",
            "Endocytosis of macromolecules"
        ],
        "answer_index": 0,
        "explanation": (
            "Non-diffusible charged particles cause unequal distribution of diffusible ions, contributing to osmotic and electrical gradients."
        ),
    },

    # =====================
    # Epithelium & Glands
    # =====================
    {
        "id": 610,
        "topic": "Epithelium & Glands",
        "question": "Which epithelial specialisation is essential for movement of mucus in the trachea?",
        "options": [
            "Cilia",
            "Microvilli",
            "Keratin",
            "Stereocilia"
        ],
        "answer_index": 0,
        "explanation": (
            "Cilia beat in a coordinated fashion to move mucus and trapped particles towards the pharynx."
        ),
    },
    {
        "id": 611,
        "topic": "Epithelium & Glands",
        "question": "Which epithelium is best adapted for rapid filtration, for example in Bowman's capsule?",
        "options": [
            "Simple squamous epithelium",
            "Stratified squamous epithelium",
            "Simple cuboidal epithelium",
            "Transitional epithelium"
        ],
        "answer_index": 0,
        "explanation": (
            "Simple squamous epithelium is thin and ideal for filtration and diffusion."
        ),
    },
    {
        "id": 612,
        "topic": "Epithelium & Glands",
        "question": "Which of the following is TRUE about epithelial regeneration?",
        "options": [
            "Most epithelia renew continuously from basal stem cells",
            "Epithelia cannot regenerate once damaged",
            "Only stratified epithelia can repair themselves",
            "Epithelia are replaced solely by fibroblasts"
        ],
        "answer_index": 0,
        "explanation": (
            "Basal cells in many epithelia divide to replace superficial cells that are shed or damaged."
        ),
    },
    {
        "id": 613,
        "topic": "Epithelium & Glands",
        "question": "Which statement about exocrine gland duct systems is TRUE?",
        "options": [
            "Compound glands have a branched duct system",
            "Simple glands have multiple main ducts",
            "All exocrine glands lack ducts",
            "Endocrine glands always have more ducts than exocrine glands"
        ],
        "answer_index": 0,
        "explanation": (
            "Simple glands have an unbranched duct; compound glands have ducts that branch."
        ),
    },
    {
        "id": 614,
        "topic": "Epithelium & Glands",
        "question": "Which cell junction anchors intermediate filaments to help resist mechanical stress?",
        "options": [
            "Desmosome",
            "Tight junction",
            "Gap junction",
            "Hemidesmosome only"
        ],
        "answer_index": 0,
        "explanation": (
            "Desmosomes link intermediate filaments between neighbouring cells and provide strong mechanical adhesion."
        ),
    },

    # =====================================
    # Connective Tissue, Cartilage & Bone
    # =====================================
    {
        "id": 615,
        "topic": "Connective Tissue, Cartilage & Bone",
        "question": "Plasma cells in connective tissue are specialised for:",
        "options": [
            "Producing antibodies",
            "Storing triglycerides",
            "Phagocytosis of bacteria",
            "Producing histamine"
        ],
        "answer_index": 0,
        "explanation": (
            "Plasma cells are derived from B lymphocytes and secrete antibodies (immunoglobulins)."
        ),
    },
    {
        "id": 616,
        "topic": "Connective Tissue, Cartilage & Bone",
        "question": "Brown adipose tissue is particularly important in:",
        "options": [
            "Non-shivering thermogenesis in newborns",
            "Long-term triglyceride storage in adults only",
            "Formation of bone marrow cavities",
            "Production of synovial fluid"
        ],
        "answer_index": 0,
        "explanation": (
            "Brown fat generates heat, especially in newborns, due to abundant mitochondria and uncoupling protein."
        ),
    },
    {
        "id": 617,
        "topic": "Connective Tissue, Cartilage & Bone",
        "question": "Which statement about cartilage is TRUE?",
        "options": [
            "It is avascular and nourished by diffusion",
            "It is richly vascularised",
            "It has a high density of nerve endings",
            "It is constantly replaced by bone in adults"
        ],
        "answer_index": 0,
        "explanation": (
            "Cartilage is avascular; nutrients diffuse through the matrix from surrounding tissues or synovial fluid."
        ),
    },
    {
        "id": 618,
        "topic": "Connective Tissue, Cartilage & Bone",
        "question": "Which bone feature contains blood vessels and nerves running longitudinally through compact bone?",
        "options": [
            "Haversian (central) canal",
            "Lacuna",
            "Canaliculus",
            "Epiphyseal plate"
        ],
        "answer_index": 0,
        "explanation": (
            "Each osteon has a central Haversian canal containing vessels and nerves."
        ),
    },
    {
        "id": 619,
        "topic": "Connective Tissue, Cartilage & Bone",
        "question": "Endochondral ossification begins with:",
        "options": [
            "A cartilage model that is gradually replaced by bone",
            "Direct bone formation from mesenchyme",
            "Intramembranous deposition of bone matrix only",
            "Replacement of bone by cartilage"
        ],
        "answer_index": 0,
        "explanation": (
            "Most long bones develop from a hyaline cartilage model that is replaced by bone in endochondral ossification."
        ),
    },

    # =================
    # Joints & Muscle
    # =================
    {
        "id": 620,
        "topic": "Joints & Muscle",
        "question": "Which of the following is a biaxial synovial joint?",
        "options": [
            "Saddle joint of the thumb",
            "Hinge joint of the elbow",
            "Pivot joint of the atlas and axis",
            "Ball-and-socket joint of the hip"
        ],
        "answer_index": 0,
        "explanation": (
            "Saddle joints, like the first carpometacarpal joint, allow movement in two planes (biaxial)."
        ),
    },
    {
        "id": 621,
        "topic": "Joints & Muscle",
        "question": "Menisci in the knee joint are composed of:",
        "options": [
            "Fibrocartilage",
            "Elastic cartilage",
            "Hyaline cartilage",
            "Dense regular connective tissue"
        ],
        "answer_index": 0,
        "explanation": (
            "Knee menisci are fibrocartilaginous pads that improve congruence and shock absorption."
        ),
    },
    {
        "id": 622,
        "topic": "Joints & Muscle",
        "question": "Which protein forms the thin filaments in skeletal muscle?",
        "options": [
            "Actin",
            "Myosin",
            "Tropomyosin only",
            "Titin"
        ],
        "answer_index": 0,
        "explanation": (
            "Thin filaments are primarily composed of actin, along with regulatory proteins tropomyosin and troponin."
        ),
    },
    {
        "id": 623,
        "topic": "Joints & Muscle",
        "question": "The A band of a sarcomere corresponds to:",
        "options": [
            "The length of the thick filaments (including overlap with thin filaments)",
            "The region containing only thin filaments",
            "The Z line region",
            "The H zone plus Z line"
        ],
        "answer_index": 0,
        "explanation": (
            "The A band includes the entire length of the thick filaments; the I band contains only thin filaments."
        ),
    },
    {
        "id": 624,
        "topic": "Joints & Muscle",
        "question": "During concentric isotonic contraction:",
        "options": [
            "The muscle shortens while generating tension",
            "The muscle lengthens under load",
            "The muscle length remains constant",
            "No cross-bridge cycling occurs"
        ],
        "answer_index": 0,
        "explanation": (
            "In concentric contractions, the muscle shortens as it overcomes a load. In eccentric contractions, it lengthens under load."
        ),
    },

    # ====================================
    # Nervous System (CNS & PNS)
    # ====================================
    {
        "id": 625,
        "topic": "Nervous System (CNS & PNS)",
        "question": "Which glial cells are the main immune effector cells of the CNS?",
        "options": [
            "Microglia",
            "Astrocytes",
            "Oligodendrocytes",
            "Ependymal cells"
        ],
        "answer_index": 0,
        "explanation": (
            "Microglia act as resident macrophage-like cells, removing debris and responding to injury in the CNS."
        ),
    },
    {
        "id": 626,
        "topic": "Nervous System (CNS & PNS)",
        "question": "The primary somatosensory cortex is located in the:",
        "options": [
            "Postcentral gyrus of the parietal lobe",
            "Precentral gyrus of the frontal lobe",
            "Occipital lobe",
            "Temporal lobe"
        ],
        "answer_index": 0,
        "explanation": (
            "The postcentral gyrus contains the primary somatosensory cortex, receiving touch, pain, and proprioceptive input."
        ),
    },
    {
        "id": 627,
        "topic": "Nervous System (CNS & PNS)",
        "question": "The corpus callosum is an example of:",
        "options": [
            "Commissural fibres connecting the two cerebral hemispheres",
            "Association fibres within one hemisphere",
            "Projection fibres to the spinal cord",
            "Grey matter only"
        ],
        "answer_index": 0,
        "explanation": (
            "Commissural fibres, like those in the corpus callosum, connect corresponding areas of the two hemispheres."
        ),
    },
    {
        "id": 628,
        "topic": "Nervous System (CNS & PNS)",
        "question": "Which structure is part of the brainstem?",
        "options": [
            "Pons",
            "Cerebellar cortex",
            "Basal ganglia",
            "Corpus callosum"
        ],
        "answer_index": 0,
        "explanation": (
            "The brainstem consists of midbrain, pons, and medulla oblongata."
        ),
    },
    {
        "id": 629,
        "topic": "Nervous System (CNS & PNS)",
        "question": "Saltatory conduction occurs in:",
        "options": [
            "Myelinated axons, jumping between nodes of Ranvier",
            "Unmyelinated axons only",
            "Dendrites only",
            "Cell bodies of neurons"
        ],
        "answer_index": 0,
        "explanation": (
            "In myelinated axons, action potentials 'jump' from node to node, greatly increasing conduction velocity."
        ),
    },

    # ==========
    # ANS
    # ==========
    {
        "id": 630,
        "topic": "ANS",
        "question": "Muscarinic receptors are found primarily:",
        "options": [
            "On parasympathetic effector organs",
            "At the neuromuscular junction",
            "On cell bodies in autonomic ganglia",
            "On sympathetic ganglia only"
        ],
        "answer_index": 0,
        "explanation": (
            "Muscarinic receptors mediate the effects of ACh on parasympathetic target tissues (and some sympathetic like sweat glands)."
        ),
    },
    {
        "id": 631,
        "topic": "ANS",
        "question": "Which of the following is MOST characteristic of sympathetic nervous system activation?",
        "options": [
            "Redistribution of blood flow towards skeletal muscle",
            "Marked increase in salivary watery secretion",
            "Increased peristalsis and digestion",
            "Pupillary constriction"
        ],
        "answer_index": 0,
        "explanation": (
            "Sympathetic activity shunts blood to skeletal muscle and heart, preparing for 'fight or flight'."
        ),
    },
    {
        "id": 632,
        "topic": "ANS",
        "question": "Grey rami communicantes carry:",
        "options": [
            "Postganglionic sympathetic fibres back to spinal nerves",
            "Preganglionic parasympathetic fibres",
            "Preganglionic sympathetic fibres to the chain",
            "Sensory fibres from viscera"
        ],
        "answer_index": 0,
        "explanation": (
            "Grey rami contain unmyelinated postganglionic sympathetic fibres rejoining spinal nerves for distribution to the body wall."
        ),
    },
    {
        "id": 633,
        "topic": "ANS",
        "question": "The enteric nervous system:",
        "options": [
            "Can function semi-independently to control gut motility and secretion",
            "Is purely parasympathetic",
            "Is purely sympathetic",
            "Has no integration with the CNS"
        ],
        "answer_index": 0,
        "explanation": (
            "The enteric plexuses can coordinate gut function but are modulated by both sympathetic and parasympathetic input."
        ),
    },
    {
        "id": 634,
        "topic": "ANS",
        "question": "Which organ receives both sympathetic and parasympathetic innervation?",
        "options": [
            "Heart",
            "Adrenal medulla only",
            "Most sweat glands",
            "Blood vessels of skeletal muscle only"
        ],
        "answer_index": 0,
        "explanation": (
            "The heart has dual autonomic innervation: sympathetic increases rate/force; parasympathetic (vagus) decreases them."
        ),
    },

    # ===========================
    # Heart & Blood Vessels
    # ===========================
    {
        "id": 635,
        "topic": "Heart & Blood Vessels",
        "question": "Which chamber of the heart forms most of the diaphragmatic (inferior) surface?",
        "options": [
            "Both ventricles, mainly the left",
            "Right atrium only",
            "Left atrium only",
            "Right ventricle only"
        ],
        "answer_index": 0,
        "explanation": (
            "The diaphragmatic surface is formed by both ventricles, predominantly the left ventricle."
        ),
    },
    {
        "id": 636,
        "topic": "Heart & Blood Vessels",
        "question": "Which statement about the cardiac skeleton is TRUE?",
        "options": [
            "It provides electrical insulation between atria and ventricles",
            "It is composed mostly of smooth muscle",
            "It lines the coronary arteries",
            "It forms the outer fibrous pericardium"
        ],
        "answer_index": 0,
        "explanation": (
            "The fibrous cardiac skeleton anchors valves and electrically insulates atria from ventricles."
        ),
    },
    {
        "id": 637,
        "topic": "Heart & Blood Vessels",
        "question": "Which vessel is commonly used for grafting in coronary artery bypass surgery?",
        "options": [
            "Great saphenous vein",
            "Portal vein",
            "Inferior vena cava",
            "Pulmonary vein"
        ],
        "answer_index": 0,
        "explanation": (
            "The great saphenous vein is often harvested as a graft for coronary bypass procedures."
        ),
    },
    {
        "id": 638,
        "topic": "Heart & Blood Vessels",
        "question": "Which type of capillary has gaps (fenestrations) that allow higher permeability, as in endocrine organs?",
        "options": [
            "Fenestrated capillaries",
            "Continuous capillaries",
            "Sinusoidal capillaries only",
            "Lymphatic capillaries"
        ],
        "answer_index": 0,
        "explanation": (
            "Fenestrated capillaries have pores in the endothelium and are found in endocrine glands, intestines, and kidneys."
        ),
    },
    {
        "id": 639,
        "topic": "Heart & Blood Vessels",
        "question": "Sinusoids are specialised capillaries found in all of the following EXCEPT:",
        "options": [
            "Lungs",
            "Liver",
            "Spleen",
            "Bone marrow"
        ],
        "answer_index": 0,
        "explanation": (
            "Sinusoidal capillaries with large gaps are found in liver, spleen, and bone marrow but not in the lungs."
        ),
    },

    # =====================
    # Lymphatic System
    # =====================
    {
        "id": 640,
        "topic": "Lymphatic System",
        "question": "Which of the following is NOT a primary lymphoid organ?",
        "options": [
            "Spleen",
            "Thymus",
            "Bone marrow",
            "None of the above"
        ],
        "answer_index": 0,
        "explanation": (
            "Primary lymphoid organs are bone marrow and thymus; the spleen is a secondary lymphoid organ."
        ),
    },
    {
        "id": 641,
        "topic": "Lymphatic System",
        "question": "Which region is drained by the right lymphatic duct?",
        "options": [
            "Right upper quadrant of the body (right head, neck, thorax, and upper limb)",
            "Both lower limbs and abdomen",
            "Entire left side of the body",
            "Only the gastrointestinal tract"
        ],
        "answer_index": 0,
        "explanation": (
            "The right lymphatic duct drains lymph from the right upper quadrant; the thoracic duct drains the rest."
        ),
    },
    {
        "id": 642,
        "topic": "Lymphatic System",
        "question": "Which tonsils are located in the lateral walls of the oropharynx?",
        "options": [
            "Palatine tonsils",
            "Pharyngeal tonsils",
            "Lingual tonsils",
            "Tubal tonsils"
        ],
        "answer_index": 0,
        "explanation": (
            "Palatine tonsils lie in the tonsillar fossae on each side of the oropharynx."
        ),
    },
    {
        "id": 643,
        "topic": "Lymphatic System",
        "question": "The term 'lymphadenopathy' refers to:",
        "options": [
            "Disease or enlargement of lymph nodes",
            "Obstruction of lymphatic vessels only",
            "Inflammation of veins",
            "Absence of lymphoid tissue"
        ],
        "answer_index": 0,
        "explanation": (
            "Lymphadenopathy describes abnormal lymph nodes (often enlarged, tender, or firm)."
        ),
    },
    {
        "id": 644,
        "topic": "Lymphatic System",
        "question": "Which cell type is especially important for antigen presentation to T cells in lymphoid tissues?",
        "options": [
            "Dendritic cells",
            "Erythrocytes",
            "Chondrocytes",
            "Osteocytes"
        ],
        "answer_index": 0,
        "explanation": (
            "Dendritic cells are key antigen-presenting cells, initiating T-cell responses in lymphoid organs."
        ),
    },

    # =====================
    # Respiratory System
    # =====================
    {
        "id": 645,
        "topic": "Respiratory System",
        "question": "At the hilum of the lung, the structures from superior to inferior on the right side are typically:",
        "options": [
            "Bronchus, pulmonary artery, pulmonary veins",
            "Pulmonary artery, bronchus, pulmonary veins",
            "Pulmonary veins, bronchus, pulmonary artery",
            "Bronchus, pulmonary veins, pulmonary artery"
        ],
        "answer_index": 0,
        "explanation": (
            "On the right, the bronchus is usually highest, then the pulmonary artery, then the pulmonary veins."
        ),
    },
    {
        "id": 646,
        "topic": "Respiratory System",
        "question": "The carina is:",
        "options": [
            "The ridge at the bifurcation of the trachea",
            "The opening of the larynx into the pharynx",
            "The aperture of the nostrils",
            "The upper border of the thyroid cartilage"
        ],
        "answer_index": 0,
        "explanation": (
            "The carina is the cartilaginous ridge at the tracheal bifurcation into the main bronchi."
        ),
    },
    {
        "id": 647,
        "topic": "Respiratory System",
        "question": "Which cell type in the alveoli removes dust particles and debris?",
        "options": [
            "Alveolar macrophages",
            "Type I pneumocytes",
            "Type II pneumocytes",
            "Goblet cells"
        ],
        "answer_index": 0,
        "explanation": (
            "Alveolar macrophages (dust cells) phagocytose inhaled particles and pathogens in the alveoli."
        ),
    },
    {
        "id": 648,
        "topic": "Respiratory System",
        "question": "Which pressure change is primarily responsible for airflow into the lungs during inspiration?",
        "options": [
            "Alveolar pressure falls below atmospheric pressure",
            "Atmospheric pressure falls below alveolar pressure",
            "Pleural pressure rises above alveolar pressure",
            "Alveolar and atmospheric pressures become equal"
        ],
        "answer_index": 0,
        "explanation": (
            "When alveolar pressure becomes slightly less than atmospheric, air flows into the lungs."
        ),
    },
    {
        "id": 649,
        "topic": "Respiratory System",
        "question": "Which structure is part of the respiratory zone where gas exchange occurs?",
        "options": [
            "Alveolar duct",
            "Terminal bronchiole",
            "Main bronchus",
            "Trachea"
        ],
        "answer_index": 0,
        "explanation": (
            "Respiratory bronchioles, alveolar ducts, and alveoli form the respiratory zone; terminal bronchioles are still conducting airways."
        ),
    },

    # =================
    # Urinary System
    # =================
    {
        "id": 650,
        "topic": "Urinary System",
        "question": "Which vessels directly form the glomerular capillary tuft?",
        "options": [
            "Afferent arterioles",
            "Efferent arterioles",
            "Interlobar arteries",
            "Renal veins"
        ],
        "answer_index": 0,
        "explanation": (
            "Afferent arterioles enter the renal corpuscle and form the glomerular capillary network."
        ),
    },
    {
        "id": 651,
        "topic": "Urinary System",
        "question": "The loop of Henle is especially important for:",
        "options": [
            "Concentrating or diluting urine by creating a medullary osmotic gradient",
            "Producing hormones such as renin",
            "Storing urine",
            "Regulating blood glucose"
        ],
        "answer_index": 0,
        "explanation": (
            "The countercurrent multiplier mechanism in the loop of Henle generates a high osmolarity in the medulla, allowing urine concentration."
        ),
    },
    {
        "id": 652,
        "topic": "Urinary System",
        "question": "Which of the following is normally NOT present in significant amounts in urine?",
        "options": [
            "Large amounts of plasma proteins",
            "Urea",
            "Creatinine",
            "Electrolytes such as Na⁺ and K⁺"
        ],
        "answer_index": 0,
        "explanation": (
            "Large plasma proteins are usually retained in the blood by the filtration barrier; their presence in urine suggests glomerular damage."
        ),
    },
    {
        "id": 653,
        "topic": "Urinary System",
        "question": "Which structure passes through the prostate in males?",
        "options": [
            "Prostatic urethra",
            "Membranous urethra",
            "Penile (spongy) urethra",
            "Ureter"
        ],
        "answer_index": 0,
        "explanation": (
            "The prostatic urethra runs through the prostate gland before continuing as the membranous and then spongy urethra."
        ),
    },
    {
        "id": 654,
        "topic": "Urinary System",
        "question": "Renin is secreted by juxtaglomerular cells in response to:",
        "options": [
            "Decreased renal perfusion pressure or low NaCl at the macula densa",
            "Increased blood pressure",
            "High plasma glucose",
            "High urine flow rate only"
        ],
        "answer_index": 0,
        "explanation": (
            "Low perfusion pressure or low distal tubular NaCl stimulates renin release, activating the renin–angiotensin–aldosterone system."
        ),
    },

    # =================
    # Endocrine System
    # =================
    {
        "id": 655,
        "topic": "Endocrine System",
        "question": "Which hormone from the posterior pituitary increases water reabsorption in the kidney?",
        "options": [
            "Antidiuretic hormone (ADH, vasopressin)",
            "Oxytocin",
            "Prolactin",
            "Growth hormone"
        ],
        "answer_index": 0,
        "explanation": (
            "ADH from the posterior pituitary acts on collecting ducts to increase water reabsorption."
        ),
    },
    {
        "id": 656,
        "topic": "Endocrine System",
        "question": "Graves’ disease is typically associated with:",
        "options": [
            "Hyperthyroidism due to autoimmune stimulation of TSH receptors",
            "Primary adrenal insufficiency",
            "Hypothyroidism due to iodine deficiency",
            "Insulin deficiency"
        ],
        "answer_index": 0,
        "explanation": (
            "Graves’ disease is an autoimmune hyperthyroidism caused by antibodies that stimulate the TSH receptor."
        ),
    },
    {
        "id": 657,
        "topic": "Endocrine System",
        "question": "Which hormone is primarily responsible for raising blood glucose during fasting?",
        "options": [
            "Glucagon",
            "Insulin",
            "Calcitonin",
            "Prolactin"
        ],
        "answer_index": 0,
        "explanation": (
            "Glucagon from pancreatic alpha cells promotes glycogenolysis and gluconeogenesis, increasing blood glucose."
        ),
    },
    {
        "id": 658,
        "topic": "Endocrine System",
        "question": "Cortisol is secreted from which part of the adrenal gland?",
        "options": [
            "Zona fasciculata of the adrenal cortex",
            "Zona glomerulosa",
            "Zona reticularis",
            "Adrenal medulla"
        ],
        "answer_index": 0,
        "explanation": (
            "The zona fasciculata primarily secretes glucocorticoids such as cortisol."
        ),
    },
    {
        "id": 659,
        "topic": "Endocrine System",
        "question": "Which hormone is essential for normal childhood growth and also affects adult metabolism?",
        "options": [
            "Growth hormone (GH)",
            "Calcitonin",
            "Oxytocin",
            "Melatonin"
        ],
        "answer_index": 0,
        "explanation": (
            "GH from the anterior pituitary is crucial for linear growth and has metabolic effects on protein, fat, and carbohydrate metabolism."
        ),
    },

    # ============================
    # Male Reproductive System
    # ============================
    {
        "id": 660,
        "topic": "Male Reproductive System",
        "question": "The acrosome of a sperm cell contains:",
        "options": [
            "Enzymes needed to penetrate the zona pellucida of the oocyte",
            "Mitochondria for ATP production",
            "DNA for fertilisation",
            "Receptors for LH"
        ],
        "answer_index": 0,
        "explanation": (
            "The acrosome is a cap-like vesicle containing enzymes that help the sperm penetrate the oocyte coverings."
        ),
    },
    {
        "id": 661,
        "topic": "Male Reproductive System",
        "question": "Which structure conveys sperm from the epididymis to the ejaculatory duct?",
        "options": [
            "Vas (ductus) deferens",
            "Ureter",
            "Urethra only",
            "Seminal vesicle"
        ],
        "answer_index": 0,
        "explanation": (
            "The vas deferens carries sperm from the epididymis to the ejaculatory duct."
        ),
    },
    {
        "id": 662,
        "topic": "Male Reproductive System",
        "question": "Which cell type forms the blood–testis barrier?",
        "options": [
            "Sertoli cells",
            "Leydig cells",
            "Spermatids",
            "Macrophages"
        ],
        "answer_index": 0,
        "explanation": (
            "Tight junctions between Sertoli cells form the blood–testis barrier, protecting developing germ cells."
        ),
    },
    {
        "id": 663,
        "topic": "Male Reproductive System",
        "question": "Testosterone is important for all of the following EXCEPT:",
        "options": [
            "Development of ovarian follicles",
            "Development of male secondary sexual characteristics",
            "Maintenance of male reproductive tract",
            "Normal spermatogenesis"
        ],
        "answer_index": 0,
        "explanation": (
            "Testosterone is not required for ovarian follicle development; it is key for male reproductive function and characteristics."
        ),
    },
    {
        "id": 664,
        "topic": "Male Reproductive System",
        "question": "Which structure contributes a small amount of mucus-rich fluid that lubricates the urethra?",
        "options": [
            "Bulbourethral (Cowper’s) glands",
            "Prostate gland",
            "Seminal vesicles",
            "Adrenal glands"
        ],
        "answer_index": 0,
        "explanation": (
            "Bulbourethral glands secrete mucus that lubricates the urethra before ejaculation."
        ),
    },

    # ==============================
    # Female Reproductive System
    # ==============================
    {
        "id": 665,
        "topic": "Female Reproductive System",
        "question": "The corpus luteum is formed from:",
        "options": [
            "The ruptured Graafian follicle after ovulation",
            "Primordial follicles",
            "Endometrial glands",
            "The uterine tube epithelium"
        ],
        "answer_index": 0,
        "explanation": (
            "After ovulation, the remnants of the Graafian follicle transform into the corpus luteum, which secretes progesterone and oestrogen."
        ),
    },
    {
        "id": 666,
        "topic": "Female Reproductive System",
        "question": "Which artery is at risk of injury in hysterectomy because it runs close to the ureter?",
        "options": [
            "Uterine artery",
            "Ovarian artery",
            "Internal pudendal artery",
            "Femoral artery"
        ],
        "answer_index": 0,
        "explanation": (
            "The uterine artery crosses superior to the ureter ('water under the bridge') near the lateral cervix."
        ),
    },
    {
        "id": 667,
        "topic": "Female Reproductive System",
        "question": "Oogenesis differs from spermatogenesis in that oogenesis:",
        "options": [
            "Produces one large ovum and polar bodies from each primary oocyte",
            "Produces four equal gametes from each primary oocyte",
            "Begins only at puberty",
            "Continues throughout life without pause"
        ],
        "answer_index": 0,
        "explanation": (
            "One primary oocyte gives rise to one functional ovum and polar bodies; spermatogenesis yields four functional sperm."
        ),
    },
    {
        "id": 668,
        "topic": "Female Reproductive System",
        "question": "Which structure is part of the vulva?",
        "options": [
            "Labia majora",
            "Uterine cavity",
            "Ovaries",
            "Fallopian tubes"
        ],
        "answer_index": 0,
        "explanation": (
            "The vulva includes external genitalia such as mons pubis, labia majora/minora, and clitoris."
        ),
    },
    {
        "id": 669,
        "topic": "Female Reproductive System",
        "question": "Human chorionic gonadotropin (hCG) is produced mainly by:",
        "options": [
            "Syncytiotrophoblast of the placenta",
            "Corpus luteum only",
            "Maternal pituitary gland",
            "Foetal liver"
        ],
        "answer_index": 0,
        "explanation": (
            "The syncytiotrophoblast secretes hCG, which maintains the corpus luteum early in pregnancy."
        ),
    },

    # ====================================
    # Cell Division & Early Embryology
    # ====================================
    {
        "id": 670,
        "topic": "Cell Division & Early Embryology",
        "question": "Which phase of the cell cycle is characterised by DNA replication?",
        "options": [
            "S phase",
            "G1 phase",
            "G2 phase",
            "M phase"
        ],
        "answer_index": 0,
        "explanation": (
            "During S phase (synthesis phase), the cell replicates its DNA in preparation for mitosis."
        ),
    },
    {
        "id": 671,
        "topic": "Cell Division & Early Embryology",
        "question": "Nondisjunction during meiosis can lead to:",
        "options": [
            "Aneuploidy such as trisomy 21",
            "Normal diploid chromosome number",
            "Formation of the three germ layers",
            "Neural tube closure"
        ],
        "answer_index": 0,
        "explanation": (
            "Failure of chromosomes to separate (nondisjunction) can result in gametes with abnormal chromosome numbers, leading to aneuploidy."
        ),
    },
    {
        "id": 672,
        "topic": "Cell Division & Early Embryology",
        "question": "The allantois in early development contributes ultimately to the formation of:",
        "options": [
            "Part of the urinary bladder",
            "The neural tube",
            "The liver",
            "The heart tube"
        ],
        "answer_index": 0,
        "explanation": (
            "The allantois is involved in early blood formation and later contributes to the formation of the urachus and bladder."
        ),
    },
    {
        "id": 673,
        "topic": "Cell Division & Early Embryology",
        "question": "Which germ layer gives rise mainly to muscles, bones, and the cardiovascular system?",
        "options": [
            "Mesoderm",
            "Ectoderm",
            "Endoderm",
            "Neural crest only"
        ],
        "answer_index": 0,
        "explanation": (
            "Mesoderm forms muscle, connective tissue, bones, and most of the cardiovascular system."
        ),
    },
    {
        "id": 674,
        "topic": "Cell Division & Early Embryology",
        "question": "The primitive streak appears in which region of the embryonic disc?",
        "options": [
            "Caudal midline of the epiblast",
            "Cranial edge of the hypoblast",
            "Lateral margin of the ectoderm",
            "Centre of the yolk sac"
        ],
        "answer_index": 0,
        "explanation": (
            "The primitive streak forms in the caudal midline of the epiblast and is essential for gastrulation."
        ),
    },
]


QUESTION_BANK = QUESTION_BANK + NEW_QUESTIONS + EXTRA_QUESTIONS + MORE_QUESTIONS + EVEN_MORE_QUESTIONS


# ----------------------------------
# TEXT SUMMARY GENERATOR (NEW)
# ----------------------------------

def generate_text_summary(responses):
    """
    Build a text summary instead of PDF.
    Returns: plain text string.
    """
    lines = []
    lines.append("Anatomy MCQ Session Summary")
    lines.append(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    lines.append(f"Total questions attempted: {len(responses)}")
    lines.append("-" * 55)

    for i, resp in enumerate(responses, start=1):
        q = resp["question"]
        selected = resp["selected_index"]
        correct_flag = resp["correct"]
        correct_idx = q["answer_index"]

        lines.append(f"\nQ{i}. [{q['topic']}] {q['question']}")
        for idx, opt in enumerate(q["options"]):
            lines.append(f"  {chr(65 + idx)}) {opt}")

        if selected is not None:
            your_ans = chr(65 + selected)
        else:
            your_ans = "Not answered"

        correct_ans = chr(65 + correct_idx)
        result = "Correct" if correct_flag else "Incorrect"

        lines.append(f"Your answer: {your_ans}")
        lines.append(f"Correct answer: {correct_ans}")
        lines.append(f"Result: {result}")
        lines.append(f"Explanation: {q['explanation']}")
        lines.append("-" * 55)

    return "\n".join(lines)


# ----------------------------------
# STREAMLIT APP (UNCHANGED LOGIC)
# ----------------------------------

st.set_page_config(page_title="Anatomy MCQ Trainer", layout="wide")

st.title("🧠 Anatomy MCQ Trainer")
st.write(
    "Use this app to drill anatomy and related basic science topics. "
    "After each question, you will see feedback and an explanation. "
    "At the end, you can download a summary of your session."
)

# Session State
if "quiz_started" not in st.session_state:
    st.session_state.quiz_started = False
if "question_order" not in st.session_state:
    st.session_state.question_order = []
if "current_q_index" not in st.session_state:
    st.session_state.current_q_index = 0
if "show_explanation" not in st.session_state:
    st.session_state.show_explanation = False
if "responses" not in st.session_state:
    st.session_state.responses = []
if "selected_option" not in st.session_state:
    st.session_state.selected_option = None
if "selected_topic" not in st.session_state:
    st.session_state.selected_topic = "All topics"

# Sidebar
all_topics = sorted(list({q["topic"] for q in QUESTION_BANK}))
topic_choice = st.sidebar.selectbox(
    "Filter by topic",
    options=["All topics"] + all_topics,
    index=(["All topics"] + all_topics).index(st.session_state.selected_topic)
)
st.session_state.selected_topic = topic_choice

num_available = len([
    q for q in QUESTION_BANK
    if topic_choice == "All topics" or q["topic"] == topic_choice
])

st.sidebar.write(f"Questions available for this selection: **{num_available}**")
shuffle_questions = st.sidebar.checkbox("Randomise order", value=True)

# Quiz start/reset
def start_quiz():
    filtered_indices = [
        i for i, q in enumerate(QUESTION_BANK)
        if st.session_state.selected_topic == "All topics"
        or q["topic"] == st.session_state.selected_topic
    ]
    if shuffle_questions:
        random.shuffle(filtered_indices)

    st.session_state.question_order = filtered_indices
    st.session_state.current_q_index = 0
    st.session_state.quiz_started = True
    st.session_state.show_explanation = False
    st.session_state.responses = []
    st.session_state.selected_option = None

if not st.session_state.quiz_started:
    st.info(
        "Select a topic in the sidebar and click **Start / Restart quiz** to begin."
    )
    if st.button("Start / Restart quiz"):
        if num_available == 0:
            st.error("No questions for this topic yet.")
        else:
            start_quiz()
else:
    if st.button("Restart quiz"):
        start_quiz()

if not st.session_state.quiz_started or len(st.session_state.question_order) == 0:
    st.stop()

# Current question
current_idx = st.session_state.current_q_index
if current_idx >= len(st.session_state.question_order):
    st.success("You have completed all questions!")
else:
    q_index = st.session_state.question_order[current_idx]
    q = QUESTION_BANK[q_index]

    st.subheader(f"Question {current_idx + 1} of {len(st.session_state.question_order)}")
    st.markdown(f"**Topic:** {q['topic']}")
    st.write(q["question"])

    options_labels = [f"{chr(65 + i)}) {opt}" for i, opt in enumerate(q["options"])]

    selected = st.radio(
        "Choose one answer:",
        options=list(range(len(q["options"]))),
        format_func=lambda i: options_labels[i],
        index=st.session_state.selected_option
        if st.session_state.selected_option is not None else 0,
        key=f"q_{q['id']}_radio"
    )
    st.session_state.selected_option = selected

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Submit answer"):
            correct = (selected == q["answer_index"])
            st.session_state.show_explanation = True

            resp = {
                "question": q,
                "selected_index": selected,
                "correct": correct,
            }
            if len(st.session_state.responses) > current_idx:
                st.session_state.responses[current_idx] = resp
            else:
                st.session_state.responses.append(resp)

    with col2:
        if st.session_state.show_explanation:
            if st.button("Next question ➜"):
                st.session_state.current_q_index += 1
                st.session_state.show_explanation = False
                st.session_state.selected_option = None
                st.experimental_rerun()

    if st.session_state.show_explanation and len(st.session_state.responses) > current_idx:
        resp = st.session_state.responses[current_idx]
        if resp["correct"]:
            st.success("✅ Correct!")
        else:
            correct_letter = chr(65 + q["answer_index"])
            st.error(f"❌ Incorrect. Correct answer is **{correct_letter}**.")
        st.markdown("**Explanation:**")
        st.write(q["explanation"])

# Summary (NO PDF, TEXT DOWNLOAD)
if st.session_state.current_q_index >= len(st.session_state.question_order):
    total = len(st.session_state.responses)
    score = sum(1 for r in st.session_state.responses if r["correct"])

    if total > 0:
        st.markdown("---")
        st.subheader("Session Summary")
        st.write(f"Questions attempted: **{total}**")
        st.write(f"Correct answers: **{score}**")
        st.write(f"Score: **{(score / total) * 100:.1f}%**")

        summary_text = generate_text_summary(st.session_state.responses)
        st.download_button(
            label="📄 Download session summary (TXT)",
            data=summary_text,
            file_name=f"anatomy_mcq_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
            mime="text/plain",
        )
    else:
        st.info("You did not answer any questions in this session.")
