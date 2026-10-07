# System Architecture: Workforce Intelligence Engine

The architecture of the Workforce Intelligence Engine (WIE) abandons traditional ad-hoc Jupyter Notebook data wrangling in favor of a **Deterministic Agent Framework**. 

Because our project explicitly **rejects false row-level joins** across unlinked datasets (which would cause severe ecological fallacies and data leakage), the architecture is fundamentally partitioned into isolated **Evidence Lanes**.

## 1. Context-Isolated Evidence Lanes

Each dataset is processed entirely independently by a specialized worker. They never share memory or indices.

```mermaid
flowchart TD
    subgraph Market Lane
        D1[(Analytics Jobs)] --> MA[Market Intelligence]
        D2[(DataScience Jobs)] --> MA
        MA --> E1[Salary/Demand Vectors]
    end
    
    subgraph Skill Lane
        D1 --> SA[Skill Intelligence]
        SA --> E2[NetworkX Ontology Graph]
    end
    
    subgraph Junior Talent Lane
        D3[(JDS Skills)] --> JA[JDS Benchmarker]
        JA --> E3[Technical Complementarity Models]
    end
    
    subgraph Senior Talent Lane
        D4[(SDS Personality)] --> SRA[SDS Benchmarker]
        SRA --> E4[Personality Interaction Models]
    end

    E1 --> ER{Evidence Registry}
    E2 --> ER
    E3 --> ER
    E4 --> ER
    
    style ER fill:#8E44AD,stroke:#fff,stroke-width:2px,color:#fff
```

## 2. ML Benchmark Engine (JDS & SDS)

The Machine Learning architecture prioritizes robustness and exact uncertainty quantification over point-estimate optimization.

```mermaid
sequenceDiagram
    participant Raw Data
    participant CV as Stratified 5-Fold (x20)
    participant Model as XGBoost / RF / LR
    participant Cal as Platt Scaler
    participant SHAP as TreeSHAP Explainer
    participant Reg as Evidence Registry

    Raw Data->>CV: Split Train/Test
    loop Inner Fold Calibration
        CV->>Model: Train Base Model
        Model->>Cal: Calibrate Probabilities
    end
    CV->>Model: Full Outer Evaluation
    Model->>SHAP: Calculate Global Feature Importance
    Model->>CV: Shuffled Target Sanity Test (Null Check)
    SHAP->>Reg: Emit Claim (Association)
    CV->>Reg: Emit Claim (ROC-AUC / ECE)
```

### Defense Against Overfitting
1. **Repeated Stratified K-Fold:** $n=139$ and $n=161$ are critically small samples. Single train/test splits are prone to seed-lottery. We use 5 folds repeated 20 times (100 discrete model evaluations per algorithm).
2. **Shuffled-Target Sanity Testing:** To prove our $0.992$ SDS AUC is not an artifact of target leakage, we scramble the target variable and re-train. The score drops immediately to $0.589$ (near random), mathematically proving the model relies on genuine feature distributions.

## 3. Skill & Natural Language Pipeline

Indian IT job postings contain highly erratic skill strings (e.g., `"python, aws, sql | big data - hyderabad"`).

```mermaid
graph LR
    A[Raw 'key_skills' String] -->|Tokenizer| B(Lowercasing & Delimiter Split)
    B --> C{Alias Dictionary}
    C -->|Match| D[Canonical Skill]
    C -->|Miss| E[Regex Fallback]
    E --> D
    D -->|Dimensional Map| F[(JDS Dimensions)]
    D -->|Co-Occurrence| G((NetworkX Graph))
```

This pipeline relies on **deterministic N-gram overlap** rather than heavy Deep Learning embeddings (like CareerBERT) to ensure lightning-fast, offline execution required by the hackathon constraints.
