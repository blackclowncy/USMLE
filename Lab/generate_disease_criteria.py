# -*- coding: utf-8 -*-
r"""
Disease Diagnostic Criteria & Evidence-Based Guidelines Compendium
Generated from Wilson's Manual of Laboratory and Diagnostic Tests (McGraw-Hill).
"""

import sys, io, re

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# We will write a comprehensive, authoritative compendium categorized by organ systems
# covering all diseases, formal diagnostic criteria, evidence-based guidelines,
# laboratory cutoffs, and clinical decision algorithms mentioned in the manual.

content = r"""# 临床疾病诊断标准与循证指南精要 (Disease Diagnostic Criteria & Evidence-Based Clinical Guidelines)

> **数据源**: 《Manual of Laboratory and Diagnostic Tests》（Author: Denise D. Wilson, PhD, APN; McGraw-Hill Medical）
> **整理用途**: USMLE Step 1 / Step 2 CK 核心疾病诊断标准、循证医学指南（The Evidence for Practice）及实验室判定阈值深度精要
> **编写说明**: 本文件系统梳理书中所有涉及具体**诊断标准（Diagnostic Criteria）**、**循证指南（Evidence-Based Practice Guidelines）**、**疾病筛查截断值（Screening & Diagnostic Cut-offs）**与**实验室判定流程（Diagnostic Workup Algorithms）**的疾病与临床病症，按系统分类编排。

---

## 目录 (Table of Contents)

1. [心血管系统疾病 (Cardiovascular Disorders)](#一心血管系统疾病-cardiovascular-disorders)
   - 1.1 急性冠脉综合征与急性心肌梗死 (Acute Coronary Syndrome & Acute Myocardial Infarction)
   - 1.2 充血性心力衰竭与失代偿性心衰 (Congestive Heart Failure & Decompensated HF)
   - 1.3 腹主动脉瘤 (Abdominal Aortic Aneurysm, AAA)
   - 1.4 深静脉血栓形成 (Deep Vein Thrombosis, DVT)
   - 1.5 肺动脉栓塞 (Pulmonary Embolism, PE)
   - 1.6 外周动脉疾病 (Peripheral Arterial Disease, PAD / Lower Extremity Perfusion)
   - 1.7 感染性心内膜炎 (Infective Endocarditis, IE)
   - 1.8 血脂异常与心血管风险分层 (Dyslipidemia & Cardiovascular Risk / NCEP ATP III)
   - 1.9 代谢综合征 (Metabolic Syndrome / ATP III Criteria)
2. [内分泌与代谢系统疾病 (Endocrine & Metabolic Disorders)](#二内分泌与代谢系统疾病-endocrine--metabolic-disorders)
   - 2.1 糖尿病 (Diabetes Mellitus, DM / ADA Criteria)
   - 2.2 糖尿病前期与糖耐量受损 (Prediabetes: IFG & IGT)
   - 2.3 妊娠期糖尿病 (Gestational Diabetes Mellitus, GDM / O'Sullivan Criteria)
   - 2.4 糖尿病肾病早期筛查 (Diabetic Nephropathy & Microalbuminuria Screening)
   - 2.5 库欣综合征 / 皮质醇增多症 (Cushing's Syndrome & Hypercortisolism)
   - 2.6 肾上腺皮质功能减退症 / 艾迪生病 (Adrenal Insufficiency & Addison's Disease)
   - 2.7 原发性醛固酮增多症 / 康恩综合征 (Primary Hyperaldosteronism / Conn's Syndrome)
   - 2.8 嗜铬细胞瘤 (Pheochromocytoma)
   - 2.9 肢端肥大症与巨人症 (Acromegaly & Gigantism)
   - 2.10 甲状腺功能亢进症与格雷夫斯病 (Hyperthyroidism & Graves' Disease)
   - 2.11 原发性与亚临床甲状腺功能减退症 (Hypothyroidism & Subclinical Hypothyroidism)
   - 2.12 原发性甲状旁腺功能亢进症 (Primary Hyperparathyroidism)
   - 2.13 男性迟发性性腺功能减退症 / 雄激素缺乏 (Male Hypogonadism / Androgen Deficiency)
3. [消化与肝胆胰系统疾病 (Gastrointestinal, Hepatic & Pancreatic Disorders)](#三消化与肝胆胰系统疾病-gastrointestinal-hepatic--pancreatic-disorders)
   - 3.1 急性胰腺炎 (Acute Pancreatitis / Revised Atlanta Criteria)
   - 3.2 结直肠癌筛查与预防 (Colorectal Cancer Screening / ACS & USPSTF Guidelines)
   - 3.3 慢性乙型与丙型病毒性肝炎 (Chronic Hepatitis B & C / AGA Guidelines)
   - 3.4 自身免疫性肝炎 (Autoimmune Hepatitis, AIH)
   - 3.5 乳糜泻 / 麦胶性肠病 (Celiac Disease / Gluten-Sensitive Enteropathy)
   - 3.6 巴雷特食管与胃食管反流病 (Barrett's Esophagus & GERD)
   - 3.7 他汀类药物相关性肝毒性 (Statin-Induced Hepatotoxicity Monitoring)
   - 3.8 持续性感染性腹泻 (Persistent Infectious Diarrhea Evaluation)
4. [肾脏与泌尿生殖系统疾病 (Renal & Genitourinary Disorders)](#四肾脏与泌尿生殖系统疾病-renal--genitourinary-disorders)
   - 4.1 慢性肾脏病 (Chronic Kidney Disease, CKD / KDOQI & KDIGO Criteria)
   - 4.2 尿路感染与急性肾盂肾炎 (Urinary Tract Infection & Pyelonephritis)
   - 4.3 输尿管结石与肾绞痛 (Ureterolithiasis & Nephrolithiasis)
   - 4.4 前列腺癌早期筛查与活检指征 (Prostate Cancer Screening / ACS Guidelines)
5. [血液与肿瘤系统疾病 (Hematologic & Oncologic Disorders)](#五血液与肿瘤系统疾病-hematologic--oncologic-disorders)
   - 5.1 弥散性血管内凝血 (Disseminated Intravascular Coagulation, DIC / ISTH Criteria)
   - 5.2 多发性骨髓瘤 (Multiple Myeloma / CRAB Criteria)
   - 5.3 肝素诱发性血小板减少症 (Heparin-Induced Thrombocytopenia, HIT / 4T Score)
   - 5.4 缺铁性贫血 (Iron Deficiency Anemia, IDA)
   - 5.5 巨幼细胞性贫血: 维生素B12与叶酸缺乏 (Megaloblastic Anemia: B12 vs. Folate Deficiency)
   - 5.6 抗凝血酶缺乏症与遗传性易栓症 (Antithrombin Deficiency & Thrombophilia)
   - 5.7 乳腺癌筛查、BRCA基因检测与活检标准 (Breast Cancer Screening, BRCA Testing & Biopsy)
   - 5.8 小细胞与非小细胞肺癌诊断分期 (Small Cell & Non-Small Cell Lung Cancer Staging)
   - 5.9 胰腺癌与卵巢癌肿瘤标志物评估 (Pancreatic & Ovarian Cancer Screening Guidelines)
6. [感染性疾病 (Infectious Diseases)](#六感染性疾病-infectious-diseases)
   - 6.1 结核感染与结核菌素皮肤试验 (Tuberculosis & Mantoux TST / PPD Criteria)
   - 6.2 人类免疫缺陷病毒感染与艾滋病 (HIV Infection & AIDS / CDC Criteria)
   - 6.3 梅毒血清学筛查与确诊 (Syphilis Serology: Screening & Confirmatory Testing)
   - 6.4 莱姆病两步法血清学诊断 (Lyme Disease / Two-Tiered Serologic Criteria)
   - 6.5 A组β溶血性链球菌性咽炎 (Group A Streptococcal Pharyngitis / Centor Criteria)
   - 6.6 传染性单核细胞增多症 (Infectious Mononucleosis / Monospot Criteria)
   - 6.7 细菌性阴道病 (Bacterial Vaginosis / Amsel Criteria)
   - 6.8 衣原体与淋球菌感染筛查 (Chlamydia & Gonorrhea Screening / USPSTF)
   - 6.9 生殖器疱疹病毒感染与剖宫产指征 (Genital Herpes Simplex Virus & Delivery Guidelines)
7. [风湿免疫与结缔组织疾病 (Rheumatologic & Autoimmune Disorders)](#七风湿免疫与结缔组织疾病-rheumatologic--autoimmune-disorders)
   - 7.1 类风湿关节炎 (Rheumatoid Arthritis / ARA 1988 & ACR Criteria)
   - 7.2 系统性红斑狼疮 (Systemic Lupus Erythematosus, SLE / ACR Criteria)
   - 7.3 痛风与假性痛风滑膜液鉴别标准 (Gout vs. Pseudogout / Synovial Crystal Analysis)
   - 7.4 重症肌无力 (Myasthenia Gravis, MG)
8. [呼吸系统与睡眠疾病 (Respiratory & Sleep Disorders)](#八呼吸系统与睡眠疾病-respiratory--sleep-disorders)
   - 8.1 慢性阻塞性肺疾病急性加重期血气分析指征 (COPD Exacerbation & ABG Indications)
   - 8.2 α1-抗胰蛋白酶缺乏症 (Alpha-1 Antitrypsin Deficiency, AATD)
   - 8.3 阻塞性睡眠呼吸暂停综合征 (Obstructive Sleep Apnea, OSA / ASDA Criteria)
9. [神经、肌肉与骨骼系统疾病 (Neurological, Musculoskeletal & Trauma)](#九神经肌肉与骨骼系统疾病-neurological-musculoskeletal--trauma)
   - 9.1 中枢神经系统感染与脑脊液鉴别诊断 (CNS Infections & CSF Differential Diagnosis)
   - 9.2 渥太华踝关节放射检查规则 (Ottawa Ankle Rules)
   - 9.3 骨质疏松症与骨量减少 (Osteoporosis & Osteopenia / WHO DEXA Criteria)
10. [妇产科与产前筛查疾病 (Obstetrics, Gynecology & Prenatal Screening)](#十妇产科与产前筛查疾病-obstetrics-gynecology--prenatal-screening)
    - 10.1 Rh血型不合与新生儿溶血病筛查 (Rh Isoimmunization Screening / USPSTF Guidelines)
    - 10.2 神经管缺陷与非整倍体产前筛查 (Neural Tube Defects & Aneuploidy Screening / MSAFP & Triple Test)
    - 10.3 羊膜穿刺术产前诊断指征 (Amniocentesis Indications / ACOG Guidelines)
    - 10.4 宫颈癌筛查指南 (Cervical Cancer Screening / ACOG & ACS Guidelines)
11. [儿科与遗传代谢疾病 (Pediatrics & Inborn Errors of Metabolism)](#十一儿科与遗传代谢疾病-pediatrics--inborn-errors-of-metabolism)
    - 11.1 苯丙酮尿症新生儿筛查 (Phenylketonuria, PKU Screening / AAFP Guidelines)
    - 11.2 儿童性虐待法医医学检验评估 (Evaluation of Suspected Sexual Abuse in Children / AAP Criteria)

---

## 一、心血管系统疾病 (Cardiovascular Disorders)

### 1.1 急性冠脉综合征与急性心肌梗死 (Acute Coronary Syndrome & Acute Myocardial Infarction)
- **权威诊断标准 / 指南来源**: ACC/AHA (American College of Cardiology / American Heart Association) 指南、欧洲心脏病学会 (ESC) 心肌梗死通用定义。
- **诊断标准与判定规则**:
  - 急性心肌梗死（AMI）的诊断需满足**心肌坏死生物标志物升高（首选心肌肌钙蛋白 cTnI / cTnT，超过正常参考上限第99百分位数）**，并伴随至少一项以下缺血证据：
    1. 缺血性临床症状（如胸骨后压榨性剧痛、放射至左肩颈或下颌）；
    2. 新发心电图缺血改变（新发 ST-T 动态改变或新发左束支传导阻滞 LBBB）；
    3. 心电图出现病理性 Q 波形成；
    4. 影像学证实新发局部室壁运动异常或存活心肌丧失；
    5. 冠脉造影证实冠状动脉内血栓形成。
- **核心实验室与标志物时间动力学**:
  - **Cardiac Troponin I (cTnI) / Troponin T (cTnT)**:
    - 升高时间: 症状发作后 3–6 小时；
    - 峰值时间: 14–24 小时；
    - 持续时间: cTnI 持续 7–10 天，cTnT 持续 10–14 天。
    - **临床意义**: 敏感度与特异度最高的心肌坏死金标准标志物。
  - **CK-MB (Creatine Kinase-MB Isoenzyme)**:
    - 升高时间: 3–6 小时；峰值: 12–24 小时；恢复: 48–72 小时。
    - **CK-MB 相对指数 (Relative Index)**: CK-MB (ng/mL) / Total CK (U/L) × 100。若比值 > 2.5%–3.0%，提示心肌损伤而非骨骼肌损伤；用于**评估心肌梗死早期再梗死 (Reinfarction)**。
  - **肌红蛋白 (Myoglobin)**:
    - 升高时间: 1–2 小时（最早升高）；阴性预测价值高；但特异性差（骨骼肌损伤亦升高）。
- **原书对应项目**: `Troponin` (P.587), `Creatine Kinase` (P.201), `Creatine Kinase-MB` (P.203), `Myoglobin` (P.418)。

---

### 1.2 充血性心力衰竭与失代偿性心衰 (Congestive Heart Failure & Decompensated HF)
- **权威诊断标准 / 指南来源**: HFSA (Heart Failure Society of America, 2006)、ACC/AHA 心力衰竭评估指南。
- **诊断标准与判定规则**:
  - 急性失代偿性心力衰竭的诊断基于临床症状（劳力性呼吸困难、端坐呼吸、阵发性夜间呼吸困难、颈静脉充盈、双下肢水肿）联合血清利钠肽（BNP / NT-proBNP）定量测定。
- **核心实验室判定阈值**:
  - **B型利钠肽 (BNP)**:
    - **< 100 pg/mL**: 心力衰竭阴性预测值极高（> 90%），基本排除心衰导致的气促；
    - **100–400 pg/mL**: 处于灰区（需结合基础肾功能、年龄、房颤、肺栓塞综合判定）；
    - **> 400 pg/mL**: 强烈支持急性心力衰竭诊断。
  - **NT-proBNP (N-末端B型利钠肽原，年龄分层排除与确诊标准)**:
    - 排除阈值: < 300 pg/mL（所有年龄段均可排除急性心衰）；
    - 确诊阈值:
      - 年龄 < 50岁: > 450 pg/mL；
      - 年龄 50–75岁: > 900 pg/mL；
      - 年龄 > 75岁: > 1800 pg/mL；
    - 肾功能不全 (eGFR < 60 mL/min): 阈值调整为 > 1200 pg/mL。
- **超声心动图标准 (Echocardiography)**:
  - 射血分数 (LVEF):
    - HFrEF (射血分数降低心衰): LVEF < 40%；
    - HFpEF (射血分数保留心衰): LVEF ≥ 50%，伴舒张功能不全及左室充盈压升高。
- **原书对应项目**: `B-Type Natriuretic Peptide` (P.420), `Echocardiography` (P.232)。

---

### 1.3 腹主动脉瘤 (Abdominal Aortic Aneurysm, AAA)
- **权威诊断标准 / 指南来源**: USPSTF (U.S. Preventive Services Task Force) 筛查推荐指南。
- **筛查与诊断标准**:
  - **USPSTF 筛查推荐**: 强烈建议对**65至75岁、有吸烟史（曾经吸烟≥100支）的男性**进行一次性腹部超声超声波（Ultrasound）筛查。
  - 对于65至75岁无吸烟史的男性，建议临床结合个体情况决定；反对对女性进行常规筛查。
- **核心超声诊断阈值**:
  - **正常腹主动脉管径**: 正常成年人管径通常 < 2.0–2.5 cm。
  - **动脉瘤定义**: 腹主动脉局限性扩张，内径 **≥ 3.0 cm**（或超过临近正常主动脉管径的 50%）。
  - **临床干预与破裂风险临界值**:
    - 直径 3.0–3.9 cm: 每年超声随访；
    - 直径 4.0–5.4 cm: 每 6 个月超声随访；
    - **直径 ≥ 5.5 cm（男性）或 ≥ 5.0 cm（女性）**，或扩张速度 **> 0.5 cm / 6个月**：达到急诊/择期血管外科手术修复（EVAR 或开腹手术）指征。
- **原书对应项目**: `Abdominal Aorta Sonogram` (P.18)。

---

### 1.4 深静脉血栓形成 (Deep Vein Thrombosis, DVT)
- **权威诊断标准 / 指南来源**: Wells DVT 临床概率评分、美国胸科医师学会 (ACCP) 指南。
- **分步诊断流程 (Stepwise Diagnostic Algorithm)**:
  1. **临床概率评估 (Wells Score for DVT)**:
     - 评分指标包括：活动性恶性肿瘤 (+1)、瘫痪或近期石膏固定 (+1)、卧床>3天或12周内大手术 (+1)、沿深静脉走行局限性压痛 (+1)、全下肢肿胀 (+1)、患侧小腿周径大于健侧>3 cm (+1)、凹陷性水肿患肢更甚 (+1)、侧支浅静脉扩张 (+1)、既往DVT史 (+1)、替代诊断概率大于或等于DVT (-2)。
     - **低度临床概率 (Low Probability / Score ≤ 0)**;
     - **中度临床概率 (Moderate Probability / Score 1–2)**;
     - **高度临床概率 (High Probability / Score ≥ 3)**。
  2. **D-二聚体 (D-Dimer)**:
     - 截断值: < 500 ng/mL FEU (纤维蛋白原等价单位)。
     - **临床规则**: 在低度或中度临床概率患者中，D-二聚体阴性可安全排除 DVT，无需行超声检查；在高度临床概率患者中，不能仅凭 D-二聚体排除，必须直接进行加压超声。
  3. **加压静脉超声 (Compression Ultrasonography, CUS)**:
     - **金标准诊断标准**: 探头压迫下**静脉内腔不能完全被压闭合 (Lack of compressibility)**，伴管腔内低回声血栓及血流多普勒信号充盈缺损。
- **原书对应项目**: `D-Dimer Test` (P.228), `Venous Doppler Ultrasound` (P.228)。

---

### 1.5 肺动脉栓塞 (Pulmonary Embolism, PE)
- **权威诊断标准 / 指南来源**: ACEP (American College of Emergency Physicians) 急诊临床实践指南、Wells PE 评分。
- **诊断标准与决策路径**:
  - **Wells PE 评分分类**:
    - 心率 > 100 次/分 (+1.5)、近期手术或卧床 (+1.5)、既往 DVT/PE 史 (+1.5)、咯血 (+1)、恶性肿瘤 (+1)、DVT 临床体征 (+3)、其他诊断可能性小于 PE (+3)。
    - 低概率 (0–1分)、中概率 (2–6分)、高概率 (≥7分)。
  - **D-二聚体检测**:
    - ACEP 推荐：在低临床概率患者中，高敏感度 D-二聚体阴性可排除 PE。
  - **CT 肺动脉造影 (CT Pulmonary Angiography, CTPA)**:
    - 现代诊断 PE 的临床金标准。诊断标准为肺动脉内充盈缺损（骑跨型血栓、完全或部分闭塞管腔）。
  - **通气/灌注核素扫描 (V/Q Scan)**:
    - 诊断标准: 高度可能性判定（≥ 2个大节段通气与灌注不匹配 Mismatched defects）。
- **原书对应项目**: `D-Dimer Test` (P.228), `CTPA` (P.388), `Lung Ventilation and Perfusion Scan` (P.388)。

---

### 1.6 外周动脉疾病 (Peripheral Arterial Disease, PAD / Lower Extremity Perfusion)
- **权威诊断标准 / 指南来源**: ACC/AHA 外周动脉疾病诊疗指南。
- **踝肱指数 (Ankle-Brachial Index, ABI) 诊断分级标准**:
  - **测定方法**: 踝部动脉收缩压（胫后动脉或足背动脉最高值）除以双上肢肱动脉收缩压最高值。
  - **分级诊断截断值**:
    - **1.00 – 1.40**: 正常外周动脉灌注；
    - **0.91 – 0.99**: 处于临界边缘状态 (Borderline)；
    - **0.71 – 0.90**: 轻度外周动脉狭窄与灌注不良 (Mild PAD)；
    - **0.41 – 0.70**: 中度外周动脉疾病 (Moderate PAD，常伴典型间歇性跛行)；
    - **≤ 0.40**: 重度缺血 (Severe PAD / Critical Limb Ischemia，常伴静息痛、组织坏死与溃疡)；
    - **> 1.40**: 血管中层钙化致血管无法被袖带压瘪 (Incompressible vessels，常见于严重糖尿病或终末期肾病，需进一步测量大趾肱指数 TBI)。
- **原书对应项目**: `Ankle-Brachial Index` (P.57)。

---

### 1.7 感染性心内膜炎 (Infective Endocarditis, IE)
- **权威诊断标准 / 指南来源**: 修正 Duke 诊断标准 (Modified Duke Criteria)。
- **诊断标准**: 满足 2项主要标准，或 1项主要标准 + 3项次要标准，或 5项次要标准者可确诊：
  - **主要标准 (Major Criteria)**:
    1. **血培养阳性**: 两次独立血培养分离出典型致病菌（草绿色链球菌、牛链球菌、HACEK 菌群、金黄色葡萄球菌、无原发病灶的肠球菌）；或持续血培养阳性（间隔12小时以上的血培养均为阳性）；或单次贝纳特柯克斯体（Q热）血培养阳性或相I IgG抗体滴度 > 1:800。
    2. **心内膜受累证据 (超声心动图阳性)**: 赘生物 (Vegetation)、瓣周脓肿 (Abscess)、新发人工瓣膜部分裂开、新发瓣膜反流。
  - **次要标准 (Minor Criteria)**:
    1. 基础心脏疾病或静脉药瘾史；
    2. 发热: 体温 ≥ 38.0°C；
    3. 血管现象: 动脉栓塞、感染性肺梗死、真菌性动脉瘤、颅内出血、结膜出血、Janeway 无痛性出血红斑；
    4. 免疫现象: 肾小球肾炎、Osler 痛性皮下结节、Roth 视网膜出血斑、类风湿因子 (RF) 阳性；
    5. 微生物学证据: 血培养阳性但不符合主要标准。
- **原书对应项目**: `Blood Culture` (P.114), `Echocardiography` (P.232), `Transesophageal Echocardiography` (P.577)。

---

### 1.8 血脂异常与心血管风险分层 (Dyslipidemia & Cardiovascular Risk / NCEP ATP III)
- **权威诊断标准 / 指南来源**: 美国国家胆固醇教育计划成人治疗组第三次报告 (NCEP ATP III)。
- **血脂异常界定标准 (Fasting Lipid Profile)**:
  - **低密度脂蛋白胆固醇 (LDL-C)**:
    - 理想水平: < 100 mg/dL (< 2.59 mmol/L)；
    - 近似理想: 100–129 mg/dL；
    - 临界升高: 130–159 mg/dL；
    - 升高: 160–189 mg/dL；
    - 极度升高: ≥ 190 mg/dL (≥ 4.90 mmol/L)。
  - **高密度脂蛋白胆固醇 (HDL-C)**:
    - 减低（危险因素）: < 40 mg/dL (< 1.04 mmol/L，男性)；< 50 mg/dL (< 1.30 mmol/L，女性)；
    - 高水平（保护因素）: ≥ 60 mg/dL (≥ 1.55 mmol/L)。
  - **甘油三酯 (Triglycerides)**:
    - 正常: < 150 mg/dL (< 1.70 mmol/L)；
    - 临界升高: 150–199 mg/dL；
    - 升高: 200–499 mg/dL；
    - 极高（急性胰腺炎高危风险）: ≥ 500 mg/dL (≥ 5.65 mmol/L)。
  - **总胆固醇 (Total Cholesterol)**:
    - 理想: < 200 mg/dL；临界: 200–239 mg/dL；高: ≥ 240 mg/dL。
- **原书对应项目**: `Lipid Profile` (P.381), `Triglycerides` (P.581), `Cholesterol` (P.184)。

---

### 1.9 代谢综合征 (Metabolic Syndrome / ATP III Criteria)
- **权威诊断标准 / 指南来源**: NCEP ATP III 及 AHA/NHLBI 诊断标准。
- **诊断标准**: 满足以下 5 项指标中至少 **3 项** 即可诊断为代谢综合征：
  1. **腹部肥胖（腰围超标）**: 男性 > 102 cm (40英寸)，女性 > 88 cm (35英寸)；
  2. **高甘油三酯血症**: 甘油三酯 ≥ 150 mg/dL (1.7 mmol/L)，或已接受药物治疗；
  3. **高密度脂蛋白降低**: 男性 HDL-C < 40 mg/dL (1.0 mmol/L)，女性 < 50 mg/dL (1.3 mmol/L)，或已接受药物治疗；
  4. **血压升高**: 收缩压 ≥ 130 mmHg 和/或 舒张压 ≥ 85 mmHg，或已确诊高血压并接受治疗；
  5. **空腹血糖受损**: 空腹血糖 ≥ 100 mg/dL (5.6 mmol/L)，或已确诊2型糖尿病并接受药物治疗。
- **原书对应项目**: `Lipid Profile` (P.381), `Glucose, Blood` (P.301)。

---

## 二、内分泌与代谢系统疾病 (Endocrine & Metabolic Disorders)

### 2.1 糖尿病 (Diabetes Mellitus, DM / ADA Criteria)
- **权威诊断标准 / 指南来源**: 美国糖尿病协会 (ADA, American Diabetes Association) 诊断指南。
- **确诊标准 (需在无明确高血糖危象情况下，非同一天重复检验确认)**:
  1. **空腹血浆血糖 (Fasting Plasma Glucose, FPG)**: **≥ 126 mg/dL (7.0 mmol/L)**（空腹定义为至少8小时内无热量摄入）；
  2. **口服葡萄糖耐量试验 (75g OGTT 2小时血糖)**: **≥ 200 mg/dL (11.1 mmol/L)**；
  3. **糖化血红蛋白 (Glycated Hemoglobin, HbA1c)**: **≥ 6.5% (48 mmol/mol)**（需采用NGSP标准化方法）；
  4. **高血糖危象或典型高血糖症状 + 随机血糖 (Random Blood Glucose)**: 存在三多一少症状（多饮、多尿、多食、体重不明原因减轻），随机血浆血糖 **≥ 200 mg/dL (11.1 mmol/L)**（单次即可确诊，无需复测）。
- **原书对应项目**: `Glucose, Blood` (P.301), `Glucose Tolerance Test` (P.305), `Glycated Hemoglobin` (P.309)。

---

### 2.2 糖尿病前期与糖耐量受损 (Prediabetes: IFG & IGT)
- **权威诊断标准 / 指南来源**: ADA 标准。
- **分类与判定阈值**:
  - **空腹血糖受损 (Impaired Fasting Glucose, IFG)**:
    - FPG: **100 – 125 mg/dL (5.6 – 6.9 mmol/L)**。
  - **糖耐量受损 (Impaired Glucose Tolerance, IGT)**:
    - 75g OGTT 2小时血糖: **140 – 199 mg/dL (7.8 – 11.0 mmol/L)**。
  - **A1C 风险区间**:
    - HbA1c: **5.7% – 6.4%**。
- **原书对应项目**: `Glucose, Blood` (P.301), `Glucose Tolerance Test` (P.305)。

---

### 2.3 妊娠期糖尿病 (Gestational Diabetes Mellitus, GDM / O'Sullivan Criteria)
- **权威诊断标准 / 指南来源**: ACOG (American College of Obstetricians and Gynecologists) & ADA 推荐的两步法筛查标准。
- **两步法筛查与诊断流程 (Two-Step Strategy)**:
  1. **第一步: 50g 葡萄糖负荷试验 (50g Glucose Challenge Test, GCT)**:
     - 孕 24–28 周进行，无需空腹。
     - 喝糖后 1 小时血糖阈值：**≥ 130 或 140 mg/dL (7.2–7.8 mmol/L)** 为阳性，需进一步行 100g 确诊试验。
  2. **第二步: 100g 3小时口服葡萄糖耐量试验 (100g 3-hr OGTT)**:
     - 需禁食 8–14 小时。根据 Carpenter-Coustan 标准，有 **≥ 2 项** 达到或超过下述界值即确诊 GDM：
       - 空腹: **≥ 95 mg/dL (5.3 mmol/L)**
       - 1 小时: **≥ 180 mg/dL (10.0 mmol/L)**
       - 2 小时: **≥ 155 mg/dL (8.6 mmol/L)**
       - 3 小时: **≥ 140 mg/dL (7.8 mmol/L)**
- **原书对应项目**: `Glucose Tolerance Test` (P.305)。

---

### 2.4 糖尿病肾病早期筛查 (Diabetic Nephropathy & Microalbuminuria Screening)
- **权威诊断标准 / 指南来源**: ADA 临床实践指南。
- **筛查策略与尿白蛋白/肌酐比值 (UACR) 标准**:
  - **筛查时机**: 1型糖尿病确诊5年后开始每年筛查；2型糖尿病确诊时立即开始每年筛查。
  - **尿微量白蛋白诊断阈值 (随机单次尿 UACR)**:
    - **正常**: UACR < 30 mg/g 肌酐 (< 3.5 mg/mmol)；
    - **微量白蛋白尿 (Microalbuminuria，早期糖尿病肾病标志)**: **30 – 299 mg/g 肌酐**；
    - **显性白蛋白尿 / 临床蛋白尿 (Macroalbuminuria / Clinical Nephropathy)**: **≥ 300 mg/g 肌酐**。
  - **判定规则**: 需在 3–6 个月内 3 次尿检中有 2 次达到上述阈值，并排除尿路感染、剧烈运动、发热等干扰因素。
- **原书对应项目**: `Microalbumin` (P.412), `Urinalysis` (P.597)。

---

### 2.5 库欣综合征 / 皮质醇增多症 (Cushing's Syndrome & Hypercortisolism)
- **权威诊断标准 / 指南来源**: 内分泌学会 (The Endocrine Society) 库欣综合征诊疗指南。
- **阶梯式实验室确诊流程**:
  1. **第一步: 证实高皮质醇血症存在 (要求至少两项初筛试验异常)**:
     - **24小时尿游离皮质醇 (24-hr Urinary Free Cortisol, UFC)**: > 正常上限的 3 倍；
     - **过夜小剂量地塞米松抑制试验 (Overnight 1-mg DST)**: 午夜11点口服地塞米松 1 mg，次晨8点血浆皮质醇 **> 1.8 mcg/dL (50 nmol/L)**（不能被抑制）；
     - **午夜唾液皮质醇 (Late-Night Salivary Cortisol)**: 失去皮质醇正常昼夜节律，午夜浓度显著升高。
  2. **第二步: ACTH 依赖性鉴别**:
     - 测定晨起血浆 ACTH 水平：
       - **ACTH < 5 pg/mL**: ACTH 非依赖性库欣（肾上腺腺瘤/腺癌，行肾上腺 CT/MRI）；
       - **ACTH > 15–20 pg/mL**: ACTH 依赖性库欣（库欣病 vs. 异位 ACTH 综合征）。
  3. **第三步: 库欣病与异位 ACTH 综合征鉴别**:
     - **大剂量地塞米松抑制试验 (High-Dose 8-mg DST)**: 库欣病（垂体腺瘤）能被抑制 ≥ 50%，异位 ACTH 不被抑制；
     - **CRH 兴奋试验**: 库欣病有 ACTH 和皮质醇跃升，异位 ACTH 无反应；
     - **岩下窦静脉取血 (IPSS)**: 垂体/外周 ACTH 浓度比值金标准。
- **原书对应项目**: `Cortisol, Blood` (P.198), `Cortisol, Urine` (P.200), `Adrenocorticotropic Hormone` (P.26), `Dexamethasone Suppression Test` (P.225)。

---

### 2.6 肾上腺皮质功能减退症 / 艾迪生病 (Adrenal Insufficiency & Addison's Disease)
- **权威诊断标准 / 指南来源**: 内分泌学会指南。
- **诊断标准与激发试验判定**:
  - **晨起基础血浆皮质醇 (8:00 AM Serum Cortisol)**:
    - **< 3 mcg/dL**: 高度怀疑肾上腺皮质功能减退；
    - **> 18–20 mcg/dL**: 可安全排除肾上腺皮质功能减退；
    - **3–18 mcg/dL**: 处于可疑区间，必须进行促肾上腺皮质激素兴奋试验。
  - **ACTH 兴奋试验 (Cosyntropin / Cortrosyn 刺激试验)**:
    - 给药: 静脉或肌注人工合成促肾上腺皮质激素 (Cosyntropin 250 mcg)；
    - 采样: 注射前基础值、注射后 30 分钟和 60 分钟采血测皮质醇。
    - **诊断标准**: 正常人峰值皮质醇应上升并 **≥ 18–20 mcg/dL**，且较基础增高至少 7 mcg/dL；**若峰值 < 18 mcg/dL，确诊为肾上腺皮质功能减退症**。
  - **原发性与继发性鉴别**:
    - **原发性 (Addison病)**: 基础 ACTH 显著升高（常 > 100 pg/mL），伴醛固酮低下、高血钾、低血钠、色素沉着；
    - **继发性 (垂体减退)**: 基础 ACTH 减低或不恰当正常，醛固酮合成保留（受RAAS调节，血钾通常正常）。
- **原书对应项目**: `Adrenocorticotropic Hormone Stimulation Test` (P.28), `Adrenocorticotropic Hormone` (P.26), `Cortisol, Blood` (P.198)。

---

### 2.7 原发性醛固酮增多症 / 康恩综合征 (Primary Hyperaldosteronism / Conn's Syndrome)
- **权威诊断标准 / 指南来源**: 内分泌学会 (The Endocrine Society) 原发性醛固酮增多症指南。
- **诊断标准与流程**:
  - **初筛试验: 醛固酮/肾素比值 (Aldosterone-to-Renin Ratio, ARR)**:
    - 条件: 清晨起床后站立 2 小时取血，停用利尿剂、ACEI/ARB、螺内酯等干扰药物；
    - **诊断界值**: **ARR > 20 – 30** (当血浆醛固酮浓度 PAC 以 ng/dL 计量，血浆肾素活性 PRA 以 ng/mL/h 计量)，且 **PAC > 15 ng/dL** 为筛查阳性。
  - **确诊试验 (抑制试验)**:
    - 生理盐水输注试验 (Saline Infusion Test) 或高钠负荷试验：正常人高容量抑制醛固酮分泌；输生理盐水后 PAC > 10 ng/dL 确诊原醛症（< 5 ng/dL 排除）。
  - **亚型定位**: 肾上腺 CT 及双侧肾上腺静脉采血 (AVS, 区别单侧腺瘤与双侧增生的金标准)。
- **原书对应项目**: `Aldosterone` (P.32), `Renin Activity, Plasma` (P.515)。

---

### 2.8 嗜铬细胞瘤 (Pheochromocytoma)
- **权威诊断标准 / 指南来源**: 内分泌学会指南。
- **实验室诊断标准与阈值**:
  - **高危疑似患者（有家族遗传综合征 MEN-2、VHL，或突发肾上腺肿物）首选**:
    - **血浆游离变肾上腺素类 (Plasma Free Metanephrines)**: 敏感度 > 97%–99%；若升高超过正常参考上限 3–4 倍，诊断高度成立。
  - **低危疑似或常规筛查患者首选**:
    - **24小时尿分级变肾上腺素和香草扁桃酸 (24-hr Urine Metanephrines & VMA)**: 特异度高达 95%–98%。
  - **影像学标准**: 实验室生化确诊后再行腹部增强 CT 或 MRI 定位；MIBG 核素扫描探查异位病灶或多发转移。
- **原书对应项目**: `Vanillylmandelic Acid and Catecholamines` (P.616), `Metanephrines` (P.410)。

---

### 2.9 肢端肥大症与巨人症 (Acromegaly & Gigantism)
- **权威诊断标准 / 指南来源**: 内分泌学会肢端肥大症指南。
- **两步法确诊标准**:
  1. **初筛指标: 血清胰岛素样生长因子-1 (Serum IGF-1)**:
     - IGF-1 生物半衰期长，浓度稳定。若血清 IGF-1 超过同年龄、同性别正常人群上限，提示肢端肥大症可能。
  2. **确诊试验: 口服葡萄糖生长激素抑制试验 (OGTT-GH Suppression Test)**:
     - 口服 75g 葡萄糖，测定 0、30、60、90、120 分钟 GH 水平。
     - **诊断标准**: 正常人高血糖反馈抑制垂体，GH 应被抑制至 **< 1.0 ng/mL**（采用高敏检测法应 **< 0.4 ng/mL**）；**若 GH 不能被抑制到该阈值以下，确诊肢端肥大症**。
  3. **垂体 MRI**: 检查垂体生长激素大腺瘤/微腺瘤。
- **原书对应项目**: `Somatomedin C / IGF-1` (P.538), `Growth Hormone` (P.312)。

---

### 2.10 甲状腺功能亢进症与格雷夫斯病 (Hyperthyroidism & Graves' Disease)
- **权威诊断标准 / 指南来源**: ATA (American Thyroid Association) / AACE 甲状腺疾病指南。
- **诊断标准与实验室模式**:
  - **原发性甲亢**:
    - **促甲状腺激素 (TSH)**: 显著受抑，通常 **< 0.01 – 0.1 mIU/L**；
    - **游离甲状腺素 (Free T4) 和/或 游离三碘甲状腺原氨酸 (Free T3)**: 显著升高。
  - **亚临床甲亢**: TSH 低于正常，但 Free T4 和 Free T3 处于正常区间。
  - **格雷夫斯病 (Graves' Disease) 病因确诊**:
    - 促甲状腺激素受体抗体 (TRAb / TSI) 阳性；
    - 放射性碘摄取率 (RAIU): 24小时摄碘率弥漫性对称性增高。
- **原书对应项目**: `Thyroid-Stimulating Hormone` (P.564), `Thyroxine, Free` (P.567), `Thyroid Uptake and Scan` (P.500)。

---

### 2.11 原发性与亚临床甲状腺功能减退症 (Hypothyroidism & Subclinical Hypothyroidism)
- **权威诊断标准 / 指南来源**: ATA / AACE 指南。
- **诊断标准与分型**:
  - **临床型原发性甲减**:
    - **血清 TSH**: 显著升高（通常 **> 10 mIU/L**）；
    - **游离 T4 (Free T4)**: 降低；
  - **亚临床甲减 (Subclinical Hypothyroidism)**:
    - **血清 TSH**: 轻至中度升高（通常 **> 4.5–5.0 mIU/L** 但 < 10 mIU/L）；
    - **游离 T4 (Free T4)**: 严格处于正常参考范围内。
  - **桥本甲状腺炎 (Hashimoto Thyroiditis) 自身免疫依据**:
    - 抗甲状腺过氧化物酶抗体 (Anti-TPO) 与抗甲状腺球蛋白抗体 (Anti-Tg) 强阳性。
- **原书对应项目**: `Thyroid-Stimulating Hormone` (P.564), `Thyroxine, Free` (P.567), `Thyroid Antibodies` (P.561)。

---

### 2.12 原发性甲状旁腺功能亢进症 (Primary Hyperparathyroidism)
- **权威诊断标准 / 指南来源**: 内分泌代谢学会指南。
- **核心实验室生化特征**:
  1. **高血钙 (Hypercalcemia)**: 血清游离钙或总钙校正值（总钙 + 0.8 × [4.0 - 白蛋白]）持续高于正常上限（> 10.2–10.5 mg/dL）；
  2. **甲状旁腺激素 (Intact PTH) 不恰当升高或处于正常高限**: 在高钙血症背景下，正常垂体-甲状旁腺轴生理反馈应彻底抑制 PTH。若 PTH 仍高于正常或处于“不恰当的正常值（Inappropriately normal）”，确诊原发性甲旁亢；
  3. **低血磷 (Hypophosphatemia)**: 尿磷排泄增加导致血磷通常低于 2.5 mg/dL；
  4. **高尿钙 (Hypercalciuria)**: 24小时尿钙通常 > 250–300 mg（用于与家族性低尿钙性高钙血症 FHH 鉴别，FHH 钙/肌酐清除比 < 0.01）。
- **原书对应项目**: `Parathyroid Hormone` (P.436), `Calcium, Blood` (P.142), `Phosphorus` (P.448)。

---

### 2.13 男性迟发性性腺功能减退症 / 雄激素缺乏 (Male Hypogonadism / Androgen Deficiency)
- **权威诊断标准 / 指南来源**: 美国内分泌学会工作组 (The Endocrine Society Task Force) 指南。
- **诊断标准**:
  - 必须同时具备**雄激素缺乏的临床症状体征**（性欲减退、勃起功能障碍、体毛稀少、骨质疏松、疲乏）以及**实验室生化证据**：
  - **清晨空腹总睾酮 (Morning Total Testosterone, 8:00–10:00 AM)**:
    - 必须在至少 **两次不同清晨** 测定均显示低于正常成人男性参考下限（通常 **< 300 ng/dL 或 < 10.4 nmol/L**）。
  - **后续分型**:
    - 测定血清 LH 和 FSH：
      - **原发性睾丸功能衰竭 (高促性腺激素性)**: LH、FSH 显著升高；
      - **继发性下丘脑-垂体功能障碍 (低促性腺激素性)**: LH、FSH 降低或异常处于正常低限，需进一步行垂体 MRI 检查。
- **原书对应项目**: `Testosterone` (P.550), `Luteinizing Hormone` (P.390), `Follicle-Stimulating Hormone` (P.283)。

---

## 三、消化与肝胆胰系统疾病 (Gastrointestinal, Hepatic & Pancreatic Disorders)

### 3.1 急性胰腺炎 (Acute Pancreatitis / Revised Atlanta Criteria)
- **权威诊断标准 / 指南来源**: 亚特兰大国际共识分类 (Revised Atlanta Criteria)。
- **诊断标准**: 满足以下 3 项标准中至少 **2 项** 即可明确诊断：
  1. **典型腹痛**: 突发、剧烈、持续性的上腹部刀割样疼痛，常向背部呈带状放射，弯腰抱膝位可轻度缓解；
  2. **血清胰酶显著升高**: 血清脂肪酶 (Lipase) 或淀粉酶 (Amylase) **≥ 正常上限的 3 倍 (≥ 3× ULN)**；
  3. **影像学证据**: 增强 CT、超声或 MRI 呈现急性胰腺炎典型特征（胰腺局限或弥漫性水肿肿胀、胰周渗出积液、坏死区低强化）。
- **核心实验室生化对比**:
  - **血清脂肪酶 (Lipase)**: 敏感度与特异度显著优于淀粉酶；发病 4–8 小时升高，峰值 24 小时，**持续升高 8–14 天**，尤其适用于就诊较晚的患者。
  - **血清淀粉酶 (Amylase)**: 发病 6–12 小时升高，24–48 小时达峰，**3–5 天内迅速恢复正常**；特异性较差（腮腺炎、肠缺血穿孔、肾衰均可升高）。
- **原书对应项目**: `Lipase, Serum` (P.373), `Amylase, Serum` (P.47), `CT Scan of Abdomen` (P.194)。

---

### 3.2 结直肠癌筛查与预防 (Colorectal Cancer Screening / ACS & USPSTF Guidelines)
- **权威诊断标准 / 指南来源**: USPSTF 结直肠癌筛查指南、ACS (American Cancer Society)。
- **常规人群筛查策略 (45/50岁至75岁无症状平均风险成人)**:
  - **结肠镜检查 (Colonoscopy)**: 筛查与预防的**金标准**。每 **10 年** 一次；发现息肉可直接行内镜下切除活检。
  - **粪便隐血试验 (FOBT) / 粪便免疫化学试验 (FIT)**: 每 **1 年** 一次。
  - **乙状结肠镜 (Flexible Sigmoidoscopy)**: 每 **5 年** 一次。
  - **双重对比气钡灌肠 (Double Contrast Barium Enema, DCBE)**: 当结肠镜无法完成或患者拒绝时，每 **5 年** 一次。
- **原书对应项目**: `Colonoscopy` (P.188), `Fecal Occult Blood Test` (P.477), `Barium Enema` (P.100)。

---

### 3.3 慢性乙型与丙型病毒性肝炎 (Chronic Hepatitis B & C / AGA Guidelines)
- **权威诊断标准 / 指南来源**: 美国胃肠病学会 (AGA) 与 AASLD 慢性肝炎临床实践指南。
- **实验室血清学与分子学诊断标准**:
  - **乙型肝炎 (Hepatitis B)**:
    - **慢性乙肝定义**: 乙型肝炎表面抗原 (HBsAg) 持续阳性 **> 6 个月**；
    - **复制活性评估**: HBeAg 阳性且 HBV DNA 定量 > 20,000 IU/mL；
    - **恢复/既往感染**: 抗-HBs 阳性、抗-HBc IgG 阳性；
    - **单纯疫苗接种成功**: 仅 抗-HBs 阳性（滴度 > 10 mIU/mL），其他全阴。
  - **丙型肝炎 (Hepatitis C / AGA 证据推荐)**:
    - **筛查指标**: 抗-HCV 抗体（酶联免疫法）；
    - **确诊金标准**: **高敏感度 HCV RNA 实时定量 PCR**（检测病毒血症确认现症感染）；
    - **抗病毒前指导**: 必须行 **HCV 基因分型 (Genotype 1–6)**，以决定直接抗病毒药物 (DAA) 方案及疗程。
- **原书对应项目**: `Hepatitis B Panel` (P.327), `Hepatitis C Virus Antibodies` (P.330), `Hepatitis Viral RNA` (P.332)。

---

### 3.4 自身免疫性肝炎 (Autoimmune Hepatitis, AIH)
- **权威诊断标准 / 指南来源**: 国际自身免疫性肝炎学组 (IAIHG) 简化评分系统。
- **诊断标准**: 满足综合评分（≥ 6分提示可能 AIH，≥ 7分明确诊断）：
  1. **自身抗体**:
     - ANA 或 ASMA (抗平滑肌抗体) ≥ 1:40 (1分)，≥ 1:80 (2分)；
     - 抗-LKM-1 (肝肾微粒体-1型抗体) ≥ 1:40 (2分)；
  2. **免疫球蛋白**: 血清 IgG 高于正常上限 (1分)，> 正常上限1.1倍 (2分)；
  3. **肝活检病理**: 界面性肝炎 (Interface hepatitis)、淋巴-浆细胞浸润、肝细胞花结样改变 (典型2分，兼容1分)；
  4. **病毒性肝炎标志物阴性**: 排除甲、乙、丙肝 (2分)。
- **原书对应项目**: `Smooth Muscle Antibodies` (P.536), `Antinuclear Antibody Test` (P.70), `Liver Biopsy` (P.378)。

---

### 3.5 乳糜泻 / 麦胶性肠病 (Celiac Disease / Gluten-Sensitive Enteropathy)
- **权威诊断标准 / 指南来源**: ACG (American College of Gastroenterology) 乳糜泻临床指南。
- **确诊流程与金标准**:
  1. **血清学首选筛查**:
     - **抗组织型转谷氨酰胺酶抗体 (Anti-tTG IgA)**: 敏感度与特异度均 > 95%；
     - **抗肌内膜抗体 (Anti-EMA IgA)**: 特异度接近 100%；
     - **注意事项**: 必须在**正常进食含麸质饮食（非无麸质饮食）期间采血**；同时必须测定**血清总 IgA**（以排除选择性 IgA 缺乏导致的假阴性，若 IgA 缺乏则需测定 tTG IgG 或 DGP IgG）。
  2. **组织病理确诊金标准**:
     - **小肠内镜下十二指肠降段多点黏膜活检**: 显示绒毛萎缩 (Villous atrophy)、隐窝增生 (Crypt hyperplasia) 和上皮内淋巴细胞增多 (Marsh 分级 III级)。
- **原书对应项目**: `Endomysial Antibodies` (P.238), `Gliadin Antibodies` (P.299), `Upper GI Endoscopy` (P.248)。

---

### 3.6 巴雷特食管与胃食管反流病 (Barrett's Esophagus & GERD)
- **权威诊断标准 / 指南来源**: ACG 指南。
- **诊断标准与内镜病理标准**:
  - **巴雷特食管 (Barrett's Esophagus)**: 长期慢性反流导致食管下段复层鳞状上皮被柱状上皮替代。内镜下观察到鳞柱交界（Z线）上移，且**活检组织病理证实存在特异性肠化生伴杯状细胞 (Specialized intestinal metaplasia with goblet cells)**。
  - **难治性 GERD 金标准**: 24小时动态食管 pH 监测（DeMeester 评分 > 14.72，或 pH < 4 的总时间百分比 > 4.2%）。
- **原书对应项目**: `Esophageal Manometry` (P.255), `Esophagogastroduodenoscopy (EGD)` (P.256)。

---

### 3.7 他汀类药物相关性肝毒性 (Statin-Induced Hepatotoxicity Monitoring)
- **权威诊断标准 / 指南来源**: AHA / ACC 降脂治疗临床指南。
- **监测标准与停药指征**:
  - 他汀类药物启动前常规检测基础转氨酶 (ALT / AST)。
  - 启动或剂量调整后 **6 至 12 周** 复查肝功能。
  - **肝毒性判定截断值**: 仅在血清转氨酶升高达**正常上限的 3 倍以上 (ALT/AST > 3× ULN)** 且在间隔数周内重复测定仍持续增高时，方考虑由他汀引起的显著肝损伤，此时应减量或停药。轻度转氨酶升高（< 3× ULN）通常无需停药。
- **原书对应项目**: `Alanine Aminotransferase` (P.29), `Aspartate Aminotransferase` (P.82)。

---

### 3.8 持续性感染性腹泻 (Persistent Infectious Diarrhea Evaluation)
- **权威诊断标准 / 指南来源**: IDSA (Infectious Diseases Society of America) 腹泻评估指南。
- **诊断性检验指征**:
  - 对于**腹泻持续超过 7 天**的患者，尤其是免疫功能低下者、伴高热、脓血便或严重脱水者，推荐行全面病原学检验：
    1. 粪便细菌培养（沙门氏菌、志贺氏菌、空肠弯曲菌）；
    2. 难辨梭状芽孢杆菌 (C. difficile) 毒素 A/B 检测（近期抗生素暴露史者）；
    3. 粪便虫卵与寄生虫检查 (O&P Examination，蓝氏贾第鞭毛虫、隐孢子虫、溶组织阿米巴)。
- **原书对应项目**: `Stool Culture` (P.542), `Clostridium difficile Toxin` (P.178), `Stool for Ova and Parasites` (P.526)。

---

## 四、肾脏与泌尿生殖系统疾病 (Renal & Genitourinary Disorders)

### 4.1 慢性肾脏病 (Chronic Kidney Disease, CKD / KDOQI & KDIGO Criteria)
- **权威诊断标准 / 指南来源**: 国际肾脏病学组织 (KDIGO) 及美国肾脏基金会 (KDOQI) 慢性肾脏病临床实践指南。
- **诊断标准**: 肾脏结构或功能异常持续 **≥ 3 个月**，并具备以下两项中至少一项：
  1. **肾小球滤过率显著下降**: eGFR < 60 mL/min/1.73 m²（伴或不伴肾脏损伤标志物）；
  2. **肾脏损伤标志物持续存在**:
     - 蛋白尿 / 白蛋白尿（UACR ≥ 30 mg/g 或 24h 尿蛋白定量 ≥ 150 mg）；
     - 尿沉渣镜检异常（红细胞管型、白细胞管型、颗粒管型）；
     - 肾小管间质病变导致的电解质与酸碱紊乱；
     - 影像学提示肾脏结构畸形（双肾缩小、多囊肾）；
     - 肾活检病理组织学异常；
     - 肾移植病史。
- **原书对应项目**: `Creatinine, Blood` (P.205), `Blood Urea Nitrogen` (P.116), `Creatinine Clearance` (P.208), `Urinalysis` (P.597)。

---

### 4.2 尿路感染与急性肾盂肾炎 (Urinary Tract Infection & Pyelonephritis)
- **权威诊断标准 / 指南来源**: IDSA 尿路感染诊疗指南。
- **实验室微生物培养与定性诊断标准**:
  - **清洁中段尿培养 (Clean-Catch Midstream Urine C&S)**:
    - 无症状菌尿: 两次间隔清洁中段尿培养单一菌落数 **≥ 10⁵ CFU/mL**；
    - 女性急性单纯性膀胱炎（伴尿频、尿急、尿痛）: 菌落数 **≥ 10²–10³ CFU/mL** 即具有临床诊断意义；
    - 男性有症状尿路感染或肾盂肾炎: 菌落数 **≥ 10³–10⁴ CFU/mL**；
    - 耻骨上膀胱穿刺尿: 任何菌落生长（≥ 10² CFU/mL）即确诊。
  - **尿液干化学快速初筛**:
    - **白细胞酯酶 (Leukocyte Esterase)** 阳性: 提示脓尿（WBC > 5–10/高倍视野）；
    - **亚硝酸盐 (Nitrite)** 阳性: 高特异性提示存在还原硝酸盐的革兰阴性杆菌（如大肠埃希菌）。
- **原书对应项目**: `Urine Culture and Sensitivity` (P.611), `Urinalysis` (P.597)。

---

### 4.3 输尿管结石与肾绞痛 (Ureterolithiasis & Nephrolithiasis)
- **权威诊断标准 / 指南来源**: AUA (American Urological Association) / ACR 放射学会指导标准。
- **循证影像学首选与诊断标准**:
  - **首选金标准**: **腹部-盆腔无造影剂螺旋 CT (Noncontrast Spiral CT / CT Stone Protocol)**。敏感度 98%，特异度 97%，能清晰显示 1–2 mm 的微小结石，评估肾积水及结石在输尿管的具体狭窄部位。
  - **腹部平片 (KUB)**: 仅适用于已知含钙阳性结石患者的随访观察；对于未确诊急性侧腹痛患者，平片敏感度低（阴性结石如尿酸结石完全透光，小结石常被肠气遮挡）。
- **原书对应项目**: `Abdominal X-ray / KUB` (P.21), `CT of Abdomen and Pelvis` (P.194)。

---

### 4.4 前列腺癌早期筛查与活检指征 (Prostate Cancer Screening / ACS Guidelines)
- **权威诊断标准 / 指南来源**: ACS 早期前列腺癌筛查指南与 AUA 临床指南。
- **诊断标准与活检指征**:
  - **血清总前列腺特异性抗原 (Total PSA)**:
    - **< 4.0 ng/mL**: 常规正常参考区间；
    - **4.0 – 10.0 ng/mL**: 诊断“灰区”（约 25% 证实为前列腺癌，其余多为良性前列腺增生 BPH 或前列腺炎）；
    - **> 10.0 ng/mL**: 恶性肿瘤风险 > 50%，强烈活检指征。
  - **游离/总 PSA 比值 (Free-to-Total PSA Ratio, %fPSA)**:
    - 在 4.0–10.0 ng/mL 灰区内，**%fPSA < 10%–15%** 高度怀疑前列腺癌（需行活检）；**%fPSA > 25%** 多提示良性病变。
  - **确诊金标准**: 经直肠超声引导下系统性前列腺穿刺活检 (TRUS-Guided Biopsy, 通常取 10–12 针)，进行 Gleason 组织学分级评分。
- **原书对应项目**: `Prostate-Specific Antigen` (P.483), `Acid Phosphatase / PAP` (P.25)。

---

## 五、血液与肿瘤系统疾病 (Hematologic & Oncologic Disorders)

### 5.1 弥散性血管内凝血 (Disseminated Intravascular Coagulation, DIC / ISTH Criteria)
- **权威诊断标准 / 指南来源**: 国际血栓与止血学会 (ISTH) 显性 DIC 评分诊断标准。
- **评分诊断系统 (必须建立在具备引起 DIC 的基础原发病前提下)**:
  1. **血小板计数 (Platelet Count)**:
     - > 100 × 10⁹/L = 0分；
     - 50–100 × 10⁹/L = 1分；
     - < 50 × 10⁹/L = 2分；
  2. **纤维蛋白相关标志物增高 (D-二聚体 / FDP)**:
     - 无升高 = 0分；
     - 中度升高 = 2分；
     - 重度升高 = 3分；
  3. **凝血酶原时间延长 (PT Prolongation)**:
     - 延长 < 3秒 = 0分；
     - 延长 3–6秒 = 1分；
     - 延长 > 6秒 = 2分；
  4. **纤维蛋白原浓度 (Fibrinogen Level)**:
     - ≥ 100 mg/dL (1.0 g/L) = 0分；
     - **< 100 mg/dL (< 1.0 g/L)** = 1分。
  - **诊断界定**: **总积分 ≥ 5 分: 符合显性 DIC (Overt DIC)**，需每日动态重复评分。
- **原书对应项目**: `Disseminated Intravascular Coagulation Screening` (P.227), `Prothrombin Time` (P.486), `Fibrinogen` (P.276), `D-Dimer` (P.228), `Platelet Count` (P.454)。

---

### 5.2 多发性骨髓瘤 (Multiple Myeloma / CRAB Criteria)
- **权威诊断标准 / 指南来源**: 国际骨髓瘤工作组 (IMWG) CRAB 诊断标准。
- **确诊标准**: 骨髓穿刺活检证实**克隆性浆细胞浸润 ≥ 10%** 或组织活检证实为**浆细胞瘤**，且同时伴随至少一项下述 **CRAB** 终末器官损害表现：
  - **C (Hypercalcemia, 高钙血症)**: 血清钙 > 11.0 mg/dL (> 2.75 mmol/L) 或高于正常上限 > 1.0 mg/dL；
  - **R (Renal Insufficiency, 肾功能不全)**: 血清肌酐 > 2.0 mg/dL (177 umol/L) 或肌酐清除率 < 40 mL/min；
  - **A (Anemia, 贫血)**: 血红蛋白 < 10.0 g/dL 或低于正常下限 > 2.0 g/dL；
  - **B (Bone Lesions, 骨质破坏)**: 全身骨骼 X 线平片、CT、PET-CT 或 MRI 证实有 ≥ 1 处溶骨性穿凿样骨质破坏病灶。
- **核心实验室特征**:
  - 血清和/或尿蛋白电泳出现单克隆 M 蛋白带 (Monoclonal M-Spike)；
  - 尿本周蛋白 (Bence Jones Protein) 阳性；红细胞沉降率 (ESR) 极度加快（常 > 100 mm/h）。
- **原书对应项目**: `Protein Electrophoresis, Serum` (P.479), `Protein Electrophoresis, Urine` (P.481), `Bone Marrow Biopsy` (P.120), `Bence Jones Protein` (P.104)。

---

### 5.3 肝素诱发性血小板减少症 (Heparin-Induced Thrombocytopenia, HIT / 4T Score)
- **权威诊断标准 / 指南来源**: ACCP 止血与抗栓临床指南。
- **4T 临床评分系统**:
  1. **血小板减少程度 (Thrombocytopenia)**: 血小板较基线下降 > 50% 且最低值 ≥ 20 × 10⁹/L (2分)；下降 30%–50% (1分)；下降 < 30% (0分)；
  2. **发生时机 (Timing)**: 肝素暴露后 5–10 天出现，或 30 天内曾用肝素者在再暴露 1 天内骤降 (2分)；
  3. **血栓形成 (Thrombosis)**: 证实新发动静脉血栓、皮肤坏死或急性全身反应 (2分)；
  4. **排除其他血小板减少原因 (oTher causes excluded)**: 无其他明确原因 (2分)。
  - **4T 评分判定**: 6–8分 (高概率)；4–5分 (中概率)；0–3分 (低概率)。
- **确诊实验室免疫学与功能学检验**:
  - **抗-PF4/肝素复合物酶联免疫抗体 (HIT ELISA)**: 高敏感度；
  - **5-羟色胺释放试验 (Serotonin Release Assay, SRA)**: 确诊金标准功能试验。
- **原书对应项目**: `Platelet Count` (P.454), `Partial Thromboplastin Time` (P.438)。

---

### 5.4 缺铁性贫血 (Iron Deficiency Anemia, IDA)
- **权威诊断标准 / 指南来源**: WHO 与美国血液病学会 (ASH) 贫血诊断标准。
- **核心实验室鉴别指标与阈值**:
  - **血常规**: 小细胞低色素性贫血（MCV < 80 fL，MCH < 27 pg，红细胞分布宽度 RDW 显著升高）；
  - **血清铁蛋白 (Serum Ferritin)**: **< 15–30 ng/mL (< 15–30 mcg/L)**（诊断体内铁耗竭最敏感、最特异的单项生化指标；但在感染或炎症应激时作为急性时相蛋白可出现假性升高）；
  - **血清铁 (Serum Iron)**: 减低（< 50–60 mcg/dL）；
  - **总铁结合力 (Total Iron-Binding Capacity, TIBC)**: 升高（> 360–400 mcg/dL）；
  - **转铁蛋白饱和度 (Transferrin Saturation)**: **< 15% – 16%**；
  - **骨髓铁染色 (Perls 普鲁士蓝染色)**: 骨髓可染铁彻底消失（诊断金标准，极少需要采用）。
- **原书对应项目**: `Iron and Total Iron-Binding Capacity` (P.355), `Ferritin` (P.262), `Complete Blood Count` (P.192)。

---

### 5.5 巨幼细胞性贫血: 维生素B12与叶酸缺乏 (Megaloblastic Anemia: B12 vs. Folate Deficiency)
- **权威诊断标准 / 指南来源**: 国际血液学临床共识。
- **核心实验室生化特征与鉴别诊断矩阵**:
  - **共同形态学特征**: 大细胞性贫血（**MCV > 100 fL**，常 > 115 fL）；外周血涂片见红细胞大小不均、卵圆形大红细胞，以及特征性**中性粒细胞核分叶过多（Hypersegmented Neutrophils，≥ 5% 的细胞有 5 叶以上核，或单见 6 叶核）**。
  - **生化鉴别指标**:
    | 检测指标 | 维生素 B12 缺乏症 | 叶酸 (Folate) 缺乏症 |
    | :--- | :--- | :--- |
    | **血清维生素 B12 测定** | 显著减低 (< 200 pg/mL) | 正常 |
    | **血清叶酸 / 红细胞叶酸** | 正常或偏高 | 显著减低 (红细胞叶酸 < 150 ng/mL) |
    | **甲基丙二酸 (Methylmalonic Acid, MMA)** | **显著升高 (Specific)** | **严格正常** |
    | **同型半胱氨酸 (Homocysteine)** | 显著升高 | 显著升高 |
    | **神经系统症状 (脊髓亚急性联合变性)** | 频繁出现（周围神经病变、共济失调） | **不出现神经退行性病变** |
- **原书对应项目**: `Vitamin B12` (P.622), `Folic Acid` (P.280), `Homocysteine` (P.337), `Methylmalonic Acid` (P.410)。

---

### 5.6 抗凝血酶缺乏症与遗传性易栓症 (Antithrombin Deficiency & Thrombophilia)
- **权威诊断标准 / 指南来源**: ACCP 易栓症评估指南。
- **临床实践与激素管理标准**:
  - 抗凝血酶 (Antithrombin III) 活性测定: 正常为 80%–120%。
  - **循证实践指南 (The Evidence for Practice)**: 对于**通过家族筛查发现有抗凝血酶缺乏症、但既往无个人静脉血栓栓塞 (VTE) 病史的女性**，**强烈禁忌使用含雌激素的口服避孕药或激素替代治疗 (HRT)**，因其发生致死性血栓形成的相对危险度增加数倍至数十倍。妊娠期间需行预防性抗凝管理。
- **原书对应项目**: `Antithrombin III` (P.78)。

---

### 5.7 乳腺癌筛查、BRCA基因检测与活检标准 (Breast Cancer Screening, BRCA Testing & Biopsy)
- **权威诊断标准 / 指南来源**: USPSTF、ACS 与 ASCO 临床实践指南。
- **循证筛查与诊断准则**:
  1. **乳腺 X 线钼靶摄影筛查 (Mammography)**:
     - 40–50岁开始，每 1–2 年常规进行筛查。
  2. **BRCA 易感基因检测遗传咨询转诊标准 (USPSTF)**:
     - 反对对普通人群进行常规盲目基因筛查。
     - **仅推荐转诊标准**: 家族史中有极高风险家族谱系者，包括：一级亲属在50岁前确诊乳腺癌、双侧乳腺癌、同一家族中兼有乳腺癌与卵巢癌、男性亲属患乳腺癌、阿什肯纳兹犹太血统家族史。
  3. **乳腺活检术选择 (Breast Biopsy)**:
     - 循证指南明确推荐：对于临床不可触及的乳腺可疑钙化或占位，**大孔径影像引导下粗针穿刺活检 (Large-core needle biopsy)** 已取代传统细针穿刺 (FNA)，具有更高的组织学诊断准确率。
- **原书对应项目**: `Mammography` (P.402), `BRCA1 and BRCA2 Breast Cancer Gene` (P.128), `Breast Biopsy` (P.130)。

---

### 5.8 小细胞与非小细胞肺癌诊断分期 (Small Cell & Non-Small Cell Lung Cancer Staging)
- **权威诊断标准 / 指南来源**: ACCP (American College of Chest Physicians) 肺癌诊疗指南。
- **诊断标准**:
  - **小细胞肺癌 (SCLC)**: 凡临床及影像高度怀疑 SCLC 者，应以创伤最小、最具成本效益的方式（支气管镜活检、经皮肺穿刺或浅表淋巴结活检）取得明确组织病理学确诊。
  - **非小细胞肺癌 (NSCLC)**: 无远处转移证据的患者在考虑根治性手术切除前，必须行 **PET-CT 扫描或纵隔镜检查**，评估纵隔淋巴结受累情况以明确分期。
- **原书对应项目**: `Biopsy, Lung` (P.134), `PET Scan` (P.463), `Chest X-ray` (P.172)。

---

### 5.9 胰腺癌与卵巢癌肿瘤标志物评估 (Pancreatic & Ovarian Cancer Screening Guidelines)
- **权威诊断标准 / 指南来源**: USPSTF & ASCO 指南。
- **循证筛查禁忌与判定**:
  - **CA 19-9 (胰腺癌标志物)**: USPSTF **强烈建议不要对无症状普通人群使用腹部触诊、超声或 CA 19-9 进行常规胰腺癌筛查**（假阳性率高，无临床获益）。CA 19-9 仅用于已确诊胰腺癌患者的疗效监测与术后复发监测。
  - **CA-125 (卵巢癌标志物)**: USPSTF 指南指出，目前**没有任何证据表明使用 CA-125、经阴道超声或盆腔双合诊能降低无症状女性的卵巢癌死亡率**；由于卵巢癌在普通人群患病率极低，常规筛查带来大量假阳性及不必要的剖腹探查手术伤害。
- **原书对应项目**: `CA 19-9 Tumor Marker` (P.137), `CA-125 Tumor Marker` (P.138)。

---

## 六、感染性疾病 (Infectious Diseases)

### 6.1 结核感染与结核菌素皮肤试验 (Tuberculosis & Mantoux TST / PPD Criteria)
- **权威诊断标准 / 指南来源**: 美国疾病预防控制中心 (CDC) / 美国胸科学会 (ATS) 结核病诊断指南。
- **结核菌素纯蛋白衍生物 (PPD) 试验硬结直径判定标准 (注射后 48–72 小时测量)**:
  - **≥ 5 mm 判定为阳性 (高危人群)**:
    1. 人类免疫缺陷病毒 (HIV) 感染者；
    2. 近期与活动性活动性传染性结核病患者有密切接触者；
    3. 胸部 X 线平片有陈旧性纤维硬结性结核病变表现者；
    4. 器官移植接受者，或长期大剂量使用糖皮质激素（相当于泼尼松 ≥ 15 mg/天持续 1 个月以上）或其他免疫抑制剂者。
  - **≥ 10 mm 判定为阳性 (中度危险人群)**:
    1. 近 5 年内来自高流行国家的移民；
    2. 静脉注射药瘾者；
    3. 高风险聚集场所的常住人员或工作人员（监狱、养老院、医疗卫生机构、收容所）；
    4. 患有增加结核发病风险的临床基础疾病者（糖尿病、矽肺、慢性肾衰竭截瘫、胃切除术后）；
    5. 年龄 < 4 岁的婴幼儿，或暴露于高危成人的儿童与青少年。
  - **≥ 15 mm 判定为阳性 (低危人群)**:
    1. 无任何已知结核暴露或发病危险因素的健康人群。
- **活动性肺结核确诊金标准**:
  - 连续 3 次清晨深咳痰标本涂片**抗酸杆菌 (AFB) 染色阳性**及**分枝杆菌结核培养阳性**；或结核分支杆菌核酸扩增试验 (NAAT / GeneXpert PCR) 阳性。
- **原书对应项目**: `Tuberculin Skin Test` (P.588), `Acid-Fast Bacilli (AFB)` (P.23)。

---

### 6.2 人类免疫缺陷病毒感染与艾滋病 (HIV Infection & AIDS / CDC Criteria)
- **权威诊断标准 / 指南来源**: CDC 艾滋病诊断与监测标准。
- **诊断标准与确诊流程**:
  1. **HIV 感染两步法血清确诊标准**:
     - **初筛试验**: 酶联免疫吸附试验 (ELISA) / 4代抗原抗体复合试验检测 HIV-1/2 抗体与 p24 抗原；
     - **确诊试验**: 初筛阳性者必须经**免疫印迹试验 (Western Blot)** 或 HIV-1/2 分型核酸确证试验复测。Western Blot 阳性标准为出现针对至少两条主要结构蛋白带（p24、gp41、gp120/gp160）。
  2. **艾滋病期 (AIDS) 确诊界定 (CDC 定义)**:
     - 满足 HIV 确诊证据，且满足以下两项中任意一项：
       1. **外周血 CD4+ T 淋巴细胞计数 < 200 cells/uL**（或 CD4+ 淋巴细胞百分比 < 14%）；
       2. **伴随出现任何一项 AIDS 指征性机会性感染或肿瘤**:
          - 肺孢子菌肺炎 (PCP, Pneumocystis jirovecii pneumonia)
          - 食管念珠菌感染
          - 隐球菌性脑膜炎
          - 巨细胞病毒 (CMV) 视网膜炎或全身感染
          - 卡波西肉瘤 (Kaposi Sarcoma)
          - 原发性中枢神经系统淋巴瘤
          - 播散性鸟-胞内分枝杆菌复合体 (MAC) 感染。
- **原书对应项目**: `Human Immunodeficiency Virus Antibody Test` (P.339), `CD4 / CD8 T-Lymphocyte Count` (P.146), `Viral Load, HIV` (P.341)。

---

### 6.3 梅毒血清学筛查与确诊 (Syphilis Serology: Screening & Confirmatory Testing)
- **权威诊断标准 / 指南来源**: USPSTF 梅毒筛查推荐指南与 CDC 性传播疾病指南。
- **两步法血清学诊断体系**:
  1. **非梅毒螺旋体抗原血清试验 (Nontreponemal Tests，初筛与疗效监测)**:
     - **RPR (快速血浆反应素试验) / VDRL (性病研究实验室试验)**:
     - 测定抗心磷脂抗体。敏感度高，但特异度相对有限（SLE、抗磷脂综合征、发热感染、妊娠可致生物学假阳性）；
     - **抗体滴度 (如 1:32, 1:64)**: 滴度与疾病活动度直接相关；治疗后滴度呈 4 倍下降（如从 1:32 降至 1:8）代表有效治愈。
  2. **梅毒螺旋体抗原特异性试验 (Treponemal Tests，确证试验)**:
     - **FTA-ABS (荧光密螺旋体抗体吸收试验) / TP-PA (梅毒螺旋体微粒凝集试验)**:
     - 测定抗苍白密螺旋体特异性抗体。特异度接近 100%；**一旦感染通常终生保持阳性**，不能用于判断复发或治愈。
  3. **神经梅毒诊断**: 脑脊液 VDRL 阳性（高度特异性指标）。
- **原书对应项目**: `Syphilis Serology` (P.548), `Venereal Disease Research Laboratory (VDRL)` (P.548)。

---

### 6.4 莱姆病两步法血清学诊断 (Lyme Disease / Two-Tiered Serologic Criteria)
- **权威诊断标准 / 指南来源**: CDC 与 ILADS (International Lyme and Associated Diseases Society) 诊断标准。
- **两步法诊断流程**:
  - **临床确诊特例**: 在莱姆病流行区，若患者具备典型**慢性游走性红斑 (Erythema Migrans)**，直接临床确诊并启动多西环素治疗，**无需等待血清学检验**（早期抗体尚未形成，假阴性率高达 50%）。
  - **疑似神经、关节或晚期播散性莱姆病血清学检测**:
    - **第 1 步**: 酶联免疫试验 (EIA) 或免疫荧光 (IFA) 筛查；
    - **第 2 步**: 若第 1 步阳性或处于灰区，进行 **Western Blot (免疫印迹法)** 确诊：
      - 发病 ≤ 4周内: IgM Western Blot（需 3 条特异带中至少 **2 条阳性**：23 kDa, 39 kDa, 41 kDa）；
      - 发病 > 4周后: IgG Western Blot（需 10 条特异带中至少 **5 条阳性**：18, 23, 28, 30, 39, 41, 45, 58, 66, 93 kDa）。
- **原书对应项目**: `Lyme Disease Antibody` (P.392)。

---

### 6.5 A组β溶血性链球菌性咽炎 (Group A Streptococcal Pharyngitis / Centor Criteria)
- **权威诊断标准 / 指南来源**: 美国感染病学会 (IDSA) 指南与改良 Centor 临床评分标准。
- **Centor 评分系统 (评估 GABS 咽炎概率与检验指征)**:
  - **扁桃体渗出物或充血水肿** (+1分)；
  - **颈前淋巴结肿大伴压痛** (+1分)；
  - **无咳嗽症状** (+1分)；
  - **有发热病史 (体温 > 38.0°C)** (+1分)；
  - **年龄修正**: 3–14岁 (+1分)；15–44岁 (0分)；≥ 45岁 (-1分)。
- **临床决策与检验标准**:
  - **评分 0–1 分**: 极低风险（< 10%），无需检验，无需抗生素；
  - **评分 2–3 分**: 中度风险，必须进行**快速抗原检测 (RADT)**；
  - **评分 ≥ 4 分**: 高度风险，需行 RADT 并考虑经验性治疗。
  - **阴性确认规则 (循证指南)**: 儿童及青少年 RADT 阴性时，**必须补做咽拭子细菌培养 (Throat Culture)**，以防漏诊导致风湿热或肾小球肾炎并发症；成人 RADT 阴性通常无需常规补做培养。
- **原书对应项目**: `Throat Culture` (P.561), `Rapid Streptococcus Antigen Test` (P.502)。

---

### 6.6 传染性单核细胞增多症 (Infectious Mononucleosis / Monospot Criteria)
- **权威诊断标准 / 指南来源**: CDC 诊断标准。
- **经典三联征**: 发热、渗出性咽颊炎、颈后淋巴结弥漫性肿大。
- **核心实验室确诊标准**:
  1. **血常规形态学**:
     - 淋巴细胞绝对计数增高（单核-淋巴细胞占白细胞总数 > 50%）；
     - 外周血涂片出现**异型淋巴细胞 (Atypical Reactive Lymphocytes) ≥ 10%**（主要为针对 EB 病毒感染 B 细胞的反应性激活 CD8+ T 细胞）。
  2. **嗜异性抗体试验 (Heterophile Antibody Test / Monospot 试验)**:
     - 凝集羊或马红细胞阳性。儿童 < 4 岁患者假阴性率较高；
  3. **EB 病毒特异性抗体 (用于 Monospot 阴性病例鉴别)**:
     - **急性感染**: 抗衣壳抗原 IgM (Anti-VCA IgM) 强阳性，抗核抗原 (Anti-EBNA) 阴性；
     - **既往感染**: Anti-EBNA IgG 阳性，Anti-VCA IgM 阴性。
- **原书对应项目**: `Heterophile Antibodies / Monospot` (P.335), `Epstein-Barr Virus Antibodies` (P.252), `White Blood Cell Count and Differential` (P.627)。

---

### 6.7 细菌性阴道病 (Bacterial Vaginosis / Amsel Criteria)
- **权威诊断标准 / 指南来源**: Amsel 临床诊断标准。
- **诊断标准**: 满足以下 4 项特征中至少 **3 项** 即可确诊：
  1. **典型阴道分泌物**: 稀薄、均匀、灰白色、均质性分泌物，附着于阴道壁；
  2. **阴道 pH 值升高**: 阴道分泌物 pH **> 4.5**（通常为 5.0–5.5）；
  3. **胺试验阳性 (Positive Whiff / Amine Test)**: 分泌物涂片加入 10% KOH 溶液后，立即释放出难闻的“鱼腥样”三甲胺臭味；
  4. **线索细胞阳性 (Clue Cells)**: 生理盐水湿片高倍镜检下，**≥ 20% 的阴道鳞状上皮细胞表面布满加德纳菌等小杆菌**，使上皮细胞边缘呈锯齿状模糊不清。
- **原书对应项目**: `Wet Mount for Vaginal Secretions` (P.625)。

---

### 6.8 衣原体与淋球菌感染筛查 (Chlamydia & Gonorrhea Screening / USPSTF)
- **权威诊断标准 / 指南来源**: USPSTF 临床预防指南与 CDC 指南。
- **筛查推荐标准**:
  - **USPSTF 强烈推荐 (A级推荐)**: 对所有 **≤ 24 岁有性生活的女性**，以及 > 24 岁但伴有性传播感染高危因素（新性伴侣、多个性伴侣、性伴侣有性病、既往性病史）的女性，进行**常规年度沙眼衣原体与淋病奈瑟菌筛查**。
- **检测金标准**:
  - **核酸扩增检测技术 (Nucleic Acid Amplification Test, NAAT)**: 采集宫颈拭子、阴道拭子或清晨首段尿（尿液首段 20–30 mL）。NAAT 敏感度与特异度达 98%–99%，显著优于传统细菌培养。
- **原书对应项目**: `Chlamydia Culture and Smear` (P.174), `Genital Culture` (P.296)。

---

### 6.9 生殖器疱疹病毒感染与剖宫产指征 (Genital Herpes Simplex Virus & Delivery Guidelines)
- **权威诊断标准 / 指南来源**: ACOG (American College of Obstetricians and Gynecologists) 指南。
- **产科临床指南标准 (The Evidence for Practice)**:
  - 临产时生殖道活动性单纯疱疹病毒 (HSV) 感染是新生儿中枢神经系统及播散性疱疹感染的极度危险因素。
  - **剖宫产指征**:
    1. 临产或胎膜破裂时，会阴部或生殖道存在**活动性活动性疱疹皮损 (Active genital lesions)**；
    2. 临产时伴随有外生殖器疱疹发作的前驱期症状（局部疼痛、烧灼感、麻木）。
    - 凡具备上述特征的产妇**必须行剖宫产分娩**以保护新生儿。若无活动性皮损且无前驱症状，允许经阴道分娩。
- **原书对应项目**: `Herpes Simplex Virus Antibodies and Culture` (P.331)。

---

## 七、风湿免疫与结缔组织疾病 (Rheumatologic & Autoimmune Disorders)

### 7.1 类风湿关节炎 (Rheumatoid Arthritis / ARA 1988 & ACR Criteria)
- **权威诊断标准 / 指南来源**: 美国风湿病学会 (ARA 1988 / ACR) 类风湿关节炎分类标准。
- **1988 ARA 经典分类标准 (满足 7 项中至少 4 项，且标准 1–4 持续至少 6 周)**:
  1. **晨僵 (Morning Stiffness)**: 关节及其周围晨僵持续 **≥ 1 小时**，方达最大改善；
  2. **3 个或 3 个以上关节区关节炎 (Arthritis of 3 or more joint areas)**: 经医生观察到的软组织肿胀或积液（左右近端指间关节、掌指关节、腕、肘、膝、踝、跖趾关节共14处可能受累区域）；
  3. **手关节炎 (Arthritis of hand joints)**: 腕关节、掌指关节 (MCP) 或近端指间关节 (PIP) 中至少 1 处肿胀；
  4. **对称性关节炎 (Symmetric Arthritis)**: 身体双侧相同关节区同时受累；
  5. **类风湿结节 (Rheumatoid Nodules)**: 骨突起部位、伸肌表面或关节周围皮下结节；
  6. **血清类风湿因子 (Rheumatoid Factor, RF) 阳性**: 滴度超出正常对照人群的第 95 百分位数；
  7. **放射学改变 (Radiographic Changes)**: 手和腕部后前位 X 线平片见典型软骨下骨质侵蚀或受累关节骨质疏松脱钙。
- **核心抗体补充**:
  - **抗环瓜氨酸肽抗体 (Anti-CCP / ACPA)**: 敏感度与 RF 相当（约 70%–80%），但特异度高达 **95%–98%**，对早期类风湿关节炎及侵蚀性骨质破坏预后具有核心诊断价值。
- **原书对应项目**: `Rheumatoid Factor` (P.519), `Anti-Cyclic Citrullinated Peptide Antibody` (P.67), `Arthrography` (P.93)。

---

### 7.2 系统性红斑狼疮 (Systemic Lupus Erythematosus, SLE / ACR Criteria)
- **权威诊断标准 / 指南来源**: ACR 11 项分类标准（满足至少 **4 项** 确诊 SLE）。
- **11 项分类诊断标准**:
  1. **颊部红斑 (Malar Rash)**: 鼻梁跨越两侧双颊的蝶形红斑，通常鼻唇沟不受累；
  2. **盘状红斑 (Discoid Rash)**: 边缘隆起的红斑伴脱屑、毛囊角栓及萎缩性瘢痕；
  3. **光敏感 (Photosensitivity)**: 暴露于紫外线日光后引起异常皮肤红斑皮疹；
  4. **口腔溃疡 (Oral Ulcers)**: 医生观察到的无痛性口腔或鼻咽部黏膜溃疡；
  5. **非侵蚀性关节炎 (Nonerosive Arthritis)**: 累及 ≥ 2 个外周关节，表现为压痛、肿胀或积液，但无软骨侵蚀破坏；
  6. **浆膜炎 (Serositis)**: 明确的胸膜炎（胸痛、胸膜摩擦音或胸水）或心包炎（心包摩擦音、心电图改变或心包积液）；
  7. **肾脏病变 (Renal Disorder)**: 持续尿蛋白 **> 0.5 g/24小时**（或定性 > 3+），或尿镜检出现红细胞/血红蛋白/颗粒/混合管型；
  8. **神经系统病变 (Neurologic Disorder)**: 排除药物及代谢紊乱引起的抽搐发作 (Seizures) 或精神病 (Psychosis)；
  9. **血液学异常 (Hematologic Disorder)**:
     - 自身免疫性溶血性贫血（伴网织红细胞增高）；或
     - 白细胞减少（两次以上白细胞计数 < 4.0 × 10⁹/L）；或
     - 淋巴细胞减少（两次以上淋巴细胞绝对值 < 1.5 × 10⁹/L）；或
     - 血小板减少（无药物诱导下血小板 < 100 × 10⁹/L）；
  10. **免疫学异常 (Immunologic Disorder)**:
      - 抗双链 DNA 抗体 (Anti-dsDNA) 阳性；或
      - 抗 Sm 抗体 (Anti-Smith) 阳性；或
      - 抗磷脂抗体阳性（狼疮抗凝物、梅毒血清试验持续假阳性、抗心磷脂抗体）；
  11. **抗核抗体 (Antinuclear Antibody, ANA) 阳性**: 荧光抗核抗体滴度阳性（排除药物性狼疮）。
- **原书对应项目**: `Antinuclear Antibody Test` (P.70), `Anti-DNA Antibodies` (P.68), `Complement Assay (C3, C4)` (P.190), `Lupus Erythematosus Prep` (P.389)。

---

### 7.3 痛风与假性痛风滑膜液鉴别标准 (Gout vs. Pseudogout / Synovial Crystal Analysis)
- **权威诊断标准 / 指南来源**: ACR 痛风分类与关节穿刺滑膜液分析标准。
- **关节滑液偏振光显微镜分析鉴别诊断标准 (确诊金标准)**:
  | 鉴别维度 | 痛风 (Gout) | 假性痛风 (Pseudogout / CPPD) |
  | :--- | :--- | :--- |
  | **结晶化学本质** | 尿酸单钠结晶 (Monosodium Urate, MSU) | 二水焦磷酸钙结晶 (CPPD) |
  | **结晶形态学** | **针状或细棒状 (Needle-shaped)**，细胞内外均可出现 | **菱形、短棒状或多边形 (Rhomboid-shaped)** |
  | **双折光性 (Birefringence)** | **强负双折光性 (Strongly Negative Birefringent)** | **弱正双折光性 (Weakly Positive Birefringent)** |
  | **红补偿滤光片下颜色判定** | **平行于慢轴时呈黄色 (Yellow)，垂直时呈蓝色** | **平行于慢轴时呈蓝色 (Blue)，垂直时呈黄色** |
  | **影像学特征** | 软骨下穿凿样骨侵蚀伴悬挂边缘 (Overhanging edge) | 关节软骨钙质沉着症 (Chondrocalcinosis，半月板线样强回声) |
- **原书对应项目**: `Synovial Fluid Analysis / Arthrocentesis` (P.545), `Uric Acid, Blood` (P.594)。

---

### 7.4 重症肌无力 (Myasthenia Gravis, MG)
- **权威诊断标准 / 指南来源**: 神经病学临床共识与 Myasthenia Gravis Foundation of America 指南。
- **诊断标准**: 满足易疲劳性肌无力表现（晨轻暮重、眼睑下垂、复视、咀嚼无力）并结合以下客观证据：
  1. **血清自身抗体测定 (首选血清学试验)**:
     - **抗乙酰胆碱受体抗体 (Anti-AChR Antibodies)**:
       - 结合型 (Binding)、阻断型 (Blocking)、调节型 (Modulating)；全身型重症肌无力阳性率达 **85%–90%**，特异度接近 100%；
     - **抗骨骼肌特异性受体酪氨酸激酶抗体 (Anti-MuSK)**: 见于约 40%–50% 的 AChR 抗体阴性全身型患者。
  2. **腾喜龙试验 (Tensilon Test / 依酚氯铵试验)**:
     - 静脉注射短效乙酰胆碱酯酶抑制剂（依酚氯铵 2–10 mg）；
     - **阳性标准**: 30–60 秒内肌力（如下垂眼睑）迅速显著改善，维持数分钟；备好阿托品防心动过缓。
  3. **电生理试验**: 重复神经低频电刺激 (RNS, 3–5 Hz) 出现动作电位波幅递减 > 10%–15%；单纤维肌电图 (SFEMG) 抖动 (Jitter) 增宽。
  4. **胸腺 CT/MRI**: 筛查胸腺瘤 (Thymoma, 约15%合并) 或胸腺增生 (约65%合并)。
- **原书对应项目**: `Acetylcholine Receptor Antibodies` (P.22), `Tensilon Test` (P.549), `Chest CT` (P.194)。

---

## 八、呼吸系统与睡眠疾病 (Respiratory & Sleep Disorders)

### 8.1 慢性阻塞性肺疾病急性加重期血气分析指征 (COPD Exacerbation & ABG Indications)
- **权威诊断标准 / 指南来源**: GOLD (Global Initiative for Chronic Obstructive Lung Disease) 慢阻肺指南。
- **循证动脉血气分析 (ABG) 紧急采集指征 (The Evidence for Practice)**:
  - Wilson 手册循证指南明确列出，已知慢阻肺患者出现加重时，必须急查动脉血气分析的临床指征：
    1. **脉搏血氧饱和度 (SpO2) < 88%**；
    2. **既往有高碳酸血症 (Hypercapnia) 病史**；
    3. **脉搏血氧仪测定准确度存疑者**（周围循环灌注差、低体温、重度贫血）；
    4. **出现嗜睡 (Somnolence)、谵妄或意识模糊**（提示二氧化碳麻醉）；
    5. **出现濒临呼吸衰竭征象**: **呼吸频率 > 40 次/分**，或出现胸腹矛盾呼吸、辅助呼吸肌显著参与。
- **动脉血气酸碱平衡失代偿判定标准**:
  - **急性呼吸性酸中毒**: pH < 7.35 伴 PaCO2 > 45 mmHg，HCO3⁻ 正常或轻微上升；
  - **慢性代偿性呼吸性酸中毒**: pH 接近正常低限 (7.35–7.38)，PaCO2 > 50 mmHg，HCO3⁻ 显著代偿性升高 (> 30–35 mEq/L)。
- **原书对应项目**: `Arterial Blood Gases` (P.86), `Oximetry` (P.426), `Carbon Dioxide` (P.148)。

---

### 8.2 α1-抗胰蛋白酶缺乏症 (Alpha-1 Antitrypsin Deficiency, AATD)
- **权威诊断标准 / 指南来源**: ATS / ERS (European Respiratory Society) 指南。
- **诊断标准与检测指征**:
  - **高危检测人群**:
    1. **早发性肺气肿 (< 45 岁)**；
    2. **无吸烟史或极低吸烟史的严重肺气肿**；
    3. 家族成员中有 AATD 病史；
    4. 幼年不明原因肝硬化或新生儿胆汁淤积性肝炎。
  - **实验室诊断标准**:
    - **血清 AAT 浓度定量**: 正常参考范围 85–213 mg/dL (20–60 umol/L)；
    - **严重缺乏临界值**: **血清 AAT < 50–80 mg/dL (< 11 umol/L)**；
    - **基因表型分型 (Phenotyping by Isoelectric Focusing)**:
      - 正常野生型: Pi*MM；
      - 重度缺乏纯合子（肺气肿高危）: **Pi*ZZ**（血清浓度仅为正常值的 10%–15%）；
      - 中度缺乏杂合子: Pi*MZ 或 Pi*SZ。
- **原书对应项目**: `Alpha1-Antitrypsin Test` (P.37)。

---

### 8.3 阻塞性睡眠呼吸暂停综合征 (Obstructive Sleep Apnea, OSA / ASDA Criteria)
- **权威诊断标准 / 指南来源**: 美国睡眠障碍协会 (ASDA / AASM) 临床指南。
- **多导睡眠图监测 (Polysomnography, PSG) 诊断标准**:
  - **呼吸暂停低通气指数 (Apnea-Hypopnea Index, AHI)**: 每小时睡眠中呼吸暂停（口鼻气流停止 ≥ 10 秒）加低通气（气流下降 ≥ 30% 伴血氧下降 ≥ 3% 或微觉醒）的总次数。
  - **OSA 确诊标准 (满足以下任意一条)**:
    1. **AHI ≥ 5 次/小时**，且伴随以下至少一项临床表现：
       - 日间过度嗜睡 (Daytime sleepiness, Epworth 评分高)；
       - 夜间窒息感、打鼾、憋醒；
       - 伴发高血压、冠心病、卒中或心律失常；
    2. **AHI ≥ 15 次/小时**（无论有无自觉临床症状均可独立确诊）。
  - **严重程度分级**:
    - 轻度: AHI 5–14.9 次/小时；
    - 中度: AHI 15–29.9 次/小时；
    - 重度: AHI ≥ 30 次/小时。
- **原书对应项目**: `Polysomnography` (P.461), `Oximetry` (P.426)。

---

## 九、神经、肌肉与骨骼系统疾病 (Neurological, Musculoskeletal & Trauma)

### 9.1 中枢神经系统感染与脑脊液鉴别诊断 (CNS Infections & CSF Differential Diagnosis)
- **权威诊断标准 / 指南来源**: IDSA 细菌性脑膜炎诊疗指南。
- **脑脊液 (CSF) 腰穿检测综合鉴别诊断矩阵**:
  | 诊断类型 | 初压 (Opening Pressure) | 白细胞计数与分类 (WBC & Diff) | 蛋白质 (Protein) | 葡萄糖 (Glucose) | 葡萄糖比值 (CSF/Blood Glucose) | 病原学证据 |
  | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
  | **正常参考值** | 70–180 mmH₂O | 0–5 /uL (全为单核细胞) | 15–45 mg/dL | 50–75 mg/dL | **≥ 0.60** (正常高值) | 无病原体 |
  | **急性化脓性细菌性脑膜炎** | **显著升高 (> 200–300 mmH₂O)** | **极度升高 (1,000–10,000+ /uL)，中性粒细胞 > 80%** | **显著升高 (> 100–500 mg/dL)** | **显著降低 (< 40 mg/dL)** | **极度降低 (< 0.40)** | 涂片革兰染色阳性，细菌培养阳性 |
  | **病毒性 (无菌性) 脑膜炎** | 正常或轻度升高 (< 200) | 轻至中度升高 (50–500 /uL)，**单核/淋巴细胞为主** | 轻度升高 (50–100 mg/dL) | **正常** | **正常 (> 0.60)** | PCR 检出肠道病毒/HSV |
  | **结核性脑膜炎** | **显著升高 (> 250)** | 中度升高 (100–500 /uL)，**早期混合后转淋巴细胞为主** | **极度升高 (> 100–500+ mg/dL)**，静置可形成薄膜 | **显著降低 (< 30 mg/dL)** | **显著降低 (< 0.30)** | 抗酸染色阳性，结核 PCR 阳性 |
  | **隐球菌/真菌性脑膜炎** | **极度升高 (> 300)** | 中度升高 (50–500 /uL)，**淋巴细胞为主** | 显著升高 (> 100–400 mg/dL) | 降低 (< 40 mg/dL) | 降低 (< 0.40) | **墨汁染色涂片阳性**，隐球菌荚膜抗原阳性 |
- **原书对应项目**: `Lumbar Puncture and Cerebrospinal Fluid Analysis` (P.383)。

---

### 9.2 渥太华踝关节放射检查规则 (Ottawa Ankle Rules)
- **权威诊断标准 / 指南来源**: 渥太华踝部损伤放射学决策规则 (Ottawa Ankle Rules)。
- **X线摄片指征标准 (The Evidence for Practice)**:
  - 仅在有钝器伤导致的踝痛且符合以下任何一项条件时，才需要行**踝关节 X 线平片 (Ankle X-ray Series)** 检查：
    1. **外踝压痛**: 外踝后缘或外踝尖端远端 6 cm 范围内有明确骨性压痛；
    2. **内踝压痛**: 内踝后缘或内踝尖端远端 6 cm 范围内有明确骨性压痛；
    3. **无法负重**: 伤后即刻以及在急诊科就诊时，均**无法独立行走负重迈出至少 4 步**。
  - **足部平片指征 (Foot X-ray Series)**: 仅在有中足疼痛且满足第5跖骨基底部压痛、舟骨压痛或无法独立行走负重4步时进行。
  - **临床价值**: 敏感度接近 100%，大幅减少不必要的辐射与急诊医疗花费。
- **原书对应项目**: `Bone Radiography / X-ray` (P.122), `Bone Scan` (P.124)。

---

### 9.3 骨质疏松症与骨量减少 (Osteoporosis & Osteopenia / WHO DEXA Criteria)
- **权威诊断标准 / 指南来源**: 世界卫生组织 (WHO) 与 USPSTF 双能 X 线骨密度仪 (DEXA) 诊断标准。
- **USPSTF 筛查推荐**:
  - 建议对所有 **≥ 65 岁的女性** 进行常规 DEXA 骨密度筛查；对于 < 65 岁但骨折风险相当的高危绝经后女性亦应筛查。
- **WHO DEXA T-Score (T 值，与健康年轻同性别成人峰值骨量对比的标准差) 分类诊断标准**:
  - **正常骨密度 (Normal)**: **T-Score ≥ -1.0 SD**；
  - **骨量减少 (Osteopenia)**: **-2.5 SD < T-Score < -1.0 SD**；
  - **骨质疏松症 (Osteoporosis)**: **T-Score ≤ -2.5 SD**（在腰椎、股骨颈或全髋部任意一处测定）；
  - **严重 / 确立型骨质疏松症 (Severe Osteoporosis)**: **T-Score ≤ -2.5 SD 伴随至少一处脆性骨折 (Fragility Fracture)**。
- **原书对应项目**: `Bone Densitometry / DEXA Scan` (P.122)。

---

## 十、妇产科与产前筛查疾病 (Obstetrics, Gynecology & Prenatal Screening)

### 10.1 Rh血型不合与新生儿溶血病筛查 (Rh Isoimmunization Screening / USPSTF Guidelines)
- **权威诊断标准 / 指南来源**: USPSTF (A级推荐) 与 ACOG 产科临床指南。
- **筛查与免疫预防标准流程**:
  1. **初次产检 (首次妊娠门诊)**: 强烈推荐对**所有孕妇**在初次产检时常规行 **ABO 血型、Rh(D) 抗原及不完全红细胞抗体筛查 (间接抗人球蛋白试验 Indirect Coombs Test)**。
  2. **Rh(D) 阴性无致敏孕妇管理**:
     - 在 **孕 28 周** 时复查间接抗体筛查。
     - 若抗体阴性，在 **孕 28 周常规肌注抗-D 免疫球蛋白 (RhoGAM 300 mcg)**。
  3. **产后管理**:
     - 新生儿出生后取脐带血行 ABO/Rh 分型及**直接抗人球蛋白试验 (Direct Coombs Test)**；
     - 若新生儿证实为 Rh(D) 阳性，母亲必须在 **分娩后 72 小时内** 再次肌注一剂抗-D 免疫球蛋白 (300 mcg)；若发生大量胎母出血，需通过 Kleihauer-Betke 试验测算追加剂量。
- **原书对应项目**: `Blood Typing and Rh Factor` (P.118), `Coombs' Test, Direct and Indirect` (P.196)。

---

### 10.2 神经管缺陷与非整倍体产前筛查 (Neural Tube Defects & Aneuploidy Screening / MSAFP & Triple Test)
- **权威诊断标准 / 指南来源**: ACOG & USPSTF 产前筛查指南。
- **母体血清标志物筛查最佳孕周**: 孕 **15 至 20 周**（以 16–18 周最为理想）。以中位数倍数 (Multiples of the Median, MoM) 计量。
- **异常组合临床判定标准**:
  - **母血清甲胎蛋白 (MSAFP) 单独异常升高 (> 2.0 – 2.5 MoM)**:
    - **首选下一步**: 必须首先行**超声检查**排除：1. 孕周推算错误（最常见）；2. 多胎妊娠；3. 胎死宫内。
    - 若排除上述原因，高度提示：**开放性神经管缺陷 (NTD, 无脑儿、脊柱裂)**、前腹壁缺损（脐膨出、腹裂）。
    - 循证预防: 孕前每天补充 **叶酸 400 mcg**（有高危孕产史者补充 4 mg/天）可减少 70% 神经管畸形发生。
  - **三联筛查 (Triple Screen) 标志物与染色体非整倍体综合征鉴别矩阵**:
    | 疾病类型 | 母体血清 AFP | 人绒毛膜促性腺激素 (hCG) | 游离雌三醇 (uE3) | 抑制素 A (Inhibin A) |
    | :--- | :--- | :--- | :--- | :--- |
    | **开放性神经管缺陷 (NTD)** | **显著升高 (↑↑)** | 正常 | 正常 | 正常 |
    | **21-三体综合征 (唐氏综合征, Down)** | **显著降低 (↓↓)** | **显著升高 (↑↑)** | **显著降低 (↓↓)** | **显著升高 (↑↑)** |
    | **18-三体综合征 (爱德华综合征, Edwards)** | **全线降低 (↓↓)** | **全线降低 (↓↓)** | **全线降低 (↓↓)** | 通常无法测出/降低 |
- **原书对应项目**: `Alpha-Fetoprotein` (P.38), `Human Chorionic Gonadotropin` (P.343), `Estriol` (P.258)。

---

### 10.3 羊膜穿刺术产前诊断指征 (Amniocentesis Indications / ACOG Guidelines)
- **权威诊断标准 / 指南来源**: ACOG 遗传学与产前诊断委员会意见。
- **循证穿刺指征 (The Evidence for Practice)**:
  - 通常在妊娠 **15 至 18 周** 进行。明确指征包括：
    1. **孕妇分娩时年龄 ≥ 35 岁（高龄孕妇）**；
    2. 母体血清生化筛查（三联/四联筛查）或无创胎儿 DNA (NIPT) 提示染色体非整倍体高危；
    3. 既往分娩过染色体异常或神经管畸形患儿；
    4. 夫妇一方证实为平衡易位或结构性染色体异常携带者；
    5. 超声发现胎儿重大解剖畸形；
    6. 胎儿宫内感染病原学评估（弓形虫、CMV）。
  - **胎儿肺成熟度评估指标 (妊娠晚期羊水分析)**:
    - **卵磷脂/鞘磷脂比值 (L/S Ratio)**: **≥ 2.0**（糖尿病孕妇需 ≥ 2.5）提示胎儿肺脏成熟，新生儿呼吸窘迫综合征 (RDS) 发生率极低；
    - **磷脂酰甘油 (Phosphatidylglycerol, PG)**: 阳性出现强力保证肺成熟。
- **原书对应项目**: `Amniocentesis` (P.45)。

---

### 10.4 宫颈癌筛查指南 (Cervical Cancer Screening / ACOG & ACS Guidelines)
- **权威诊断标准 / 指南来源**: ACOG / ACS / USPSTF 宫颈癌筛查指南。
- **常规人群分年龄筛查标准**:
  - **年龄 < 21 岁**: **禁止筛查**（无论有无性生活史，青少年 HPV 感染率高且绝大多数可自愈，过度筛查带来宫颈物理创伤）；
  - **年龄 21 – 29 岁**: 仅行**宫颈细胞学检查 (Pap Smear 液基薄层细胞学)**，每 **3 年** 一次；**不推荐**常规进行高危型 HPV 病毒检测；
  - **年龄 30 – 65 岁**:
    - **首选推荐联合筛查**: 宫颈细胞学 + 高危型 HPV DNA 联合检测 (Co-testing)，每 **5 年** 一次；
    - 备选方案: 仅行宫颈细胞学检查，每 **3 年** 一次；
  - **年龄 > 65 岁**: 若既往筛查充分阴性（过去10年内连续3次细胞学阴性或连续2次联合阴性，最近一次在5年内），**终止筛查**；
  - **全子宫切除术后**: 因良性疾病切除子宫且无 CIN 2/3 史者，**彻底终止筛查**。
- **原书对应项目**: `Papanicolaou Smear (Pap Smear)` (P.430), `Colposcopy` (P.189), `Human Papillomavirus DNA Testing` (P.430)。

---

## 十一、儿科与遗传代谢疾病 (Pediatrics & Inborn Errors of Metabolism)

### 11.1 苯丙酮尿症新生儿筛查 (Phenylketonuria, PKU Screening / AAFP Guidelines)
- **权威诊断标准 / 指南来源**: 美国儿科学会 (AAP) 与美国家庭医师学会 (AAFP) 强力推荐。
- **筛查策略与生化诊断截断值**:
  - **采血时机**: 必须在**新生儿足量摄入母乳或配方奶蛋白饮食至少 24–48 小时之后**进行足跟采血滤纸吸附法（Guthrie 细菌生长抑制试验或串联质谱 Tandem Mass Spectrometry）；出生后立即采血假阴性率极高。
  - **血清生化确诊标准**:
    - **血浆苯丙氨酸 (Plasma Phenylalanine) 持续浓度 > 20 mg/dL (1200 umol/L)**；
    - 同时伴随血酪氨酸 (Tyrosine) 浓度减低；
    - 必须进一步测定四氢生物蝶呤 (BH4) 辅酶代谢产物以排除 BH4 缺乏型高苯丙氨酸血症。
- **原书对应项目**: `Phenylketonuria Test / Guthrie Test` (P.446)。

---

### 11.2 儿童性虐待法医医学检验评估 (Evaluation of Suspected Sexual Abuse in Children / AAP Criteria)
- **权威诊断标准 / 指南来源**: 美国儿科学会 (AAP) 疑似儿童性虐待临床法医评估指南。
- **客观法医实验室证据判定标准 (The Evidence for Practice)**:
  - 阴道口、肛周黏膜损伤及感染微生物学证据是法医评估的核心。
  - **酸性磷酸酶 (Acid Phosphatase, ACP / PAP) 活性**:
    - 人类精液中含有极高浓度的酸性磷酸酶。
    - **判定规则**: 在儿童阴道拭子、肛周拭子或衣物斑迹提取物中检出**异常高浓度的酸性磷酸酶**，AAP 指南明确将其作为向法定儿童保护机构（Child Protective Services）举报疑似性虐待的核心客观法医标准之一。
  - **病原体确诊证据**: 婴幼儿生殖道分离出淋球菌 (N. gonorrhoeae) 或沙眼衣原体（排除围产期垂直传播）。
- **原书对应项目**: `Acid Phosphatase` (P.25), `Chlamydia Culture` (P.174), `Genital Culture` (P.296)。

---

## 结语与 USMLE 复习方法建议

1. **实验室指标与病理生理机制联动**: 在 USMLE 题目中，单纯死记正常参考值意义有限，重点在于理解**反常升降背后的代偿与失代偿机制**（如：高血钙背景下出现“正常高限”的 PTH 是原发性甲旁亢的标志；严重的酸中毒呼吸代偿公式 Winter's Formula 等）。
2. **结合“循证实践指南 (The Evidence for Practice)”解题**: 本书中强调的循证指南（如他汀类转氨酶监测截断值 > 3× ULN；腹主动脉瘤男性吸烟者 65–75 岁单次超声筛查；D-二聚体在低临床概率下的排除价值；宫颈癌 < 21 岁禁止筛查等）直接对应 USMLE Step 2 CK 及 Step 3 的核心“下一步最佳临床决策 (Next Best Step in Management)”考点。
3. **查阅全书 359 项检测详情**: 请参阅同文件夹下的另一记录文件 [01_Laboratory_Tests_Manual.md](file:///D:/Github/USMLE/Lab/01_Laboratory_Tests_Manual.md)。
"""

with open("02_Disease_Diagnostic_Criteria.md", "w", encoding="utf-8") as f:
    f.write(content)

print("02_Disease_Diagnostic_Criteria.md generated successfully!")
