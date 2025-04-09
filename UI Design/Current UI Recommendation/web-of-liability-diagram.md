# Web of Liability Entity Relationships

This diagram illustrates the relationship structure between loans, legal documents, collateral, and accounts in the Farm Credit Collateral Management System.

```mermaid
flowchart LR
    subgraph Loans
        L1["LC-2023-045\nLong Term"]
        L2["LC-2023-078\nIntermediate Term"]
        L3["LC-2023-091\nShort Term"]
        L4["LC-2023-103\nLong Term"]
        L5["LC-2023-118\nIntermediate Term"]
        L6["LC-2023-129\nOperating"]
    end

    subgraph "Legal Documents"
        D1["Security Agreement\n#SA-001"]
        D2["Trust Agreement\n#TA-002"]
        D3["Security Agreement\n#SA-003"]
        D4["Security Agreement\n#SA-004"]
        D5["Trust Agreement\n#TA-005"]
        D6["UCC Filing\n#UCC-006"]
        D7["Security Agreement\n#SA-007"]
        D8["UCC Filing\n#UCC-008"]
    end

    subgraph "Real Estate"
        RE1["Davis Farm\nAgricultural Land\n120 Acres"]
        RE2["Johnson Property\nAgricultural Land\n85 Acres"]
        RE3["Smith Commercial Building\nCommercial\n15,000 sq ft"]
        RE4["Taylor Warehouse\nCommercial\n8,000 sq ft"]
        RE5["Wilson Land\nResidential\n2 Acres"]
    end

    subgraph Accounts
        A1["Smith Family Farms\nCustomer ID: 1024789"]
        A2["Smith Agricultural LLC\nCustomer ID: 1024790"]
    end
    
    subgraph "Equipment"
        EQ1["Tractor (John Deere)\nFarm Equipment"]
        EQ2["Combine Harvester\nFarm Equipment"]
        EQ3["Grain Silo\nStorage"]
        EQ4["Irrigation System\nFarm Equipment"]
    end

    subgraph "Livestock"
        LS1["Cattle Herd\n50 head"]
        LS2["Poultry Operation"]
    end
    
    %% Account ownership relationships
    A1 --> RE1
    A1 --> RE2
    A1 --> RE3
    A1 --> EQ1
    A1 --> EQ2
    A1 --> LS1
    
    %% Account borrower relationships
    A1 --> L1
    A1 --> L2
    A1 --> L3
    
    %% Account legal document relationships
    A1 --> D1
    A1 --> D2
    A1 --> D3
    A1 --> D4
    
    %% Smith Agricultural LLC relationships
    A2 --> RE4
    A2 --> RE5
    A2 --> EQ3
    A2 --> LS2
    A2 --> EQ4
    
    %% Account borrower relationships
    A2 --> L4
    A2 --> L5
    A2 --> L6
    
    %% Account legal document relationships
    A2 --> D5
    A2 --> D6
    A2 --> D7
    A2 --> D8
    
    %% Loan to legal document relationships
    L1 -- "documents" --> D1
    L2 -- "documents" --> D2
    L2 -- "documents" --> D3
    L3 -- "documents" --> D4
    L4 -- "documents" --> D5
    L4 -- "documents" --> D6
    L5 -- "documents" --> D7
    L6 -- "documents" --> D8
    
    %% Legal document to collateral relationships - high risk connections with dotted lines
    D1 -- "secures" --> RE1
    D2 -- "secures" --> RE2
    D3 -- "secures" --> EQ1
    D4 -- "secures" --> LS1
    D5 -. "high risk" .-> RE3
    D6 -- "secures" --> EQ2
    D6 -- "secures (lien pos. 2)" --> EQ2
    D7 -- "secures" --> RE4
    D7 -- "secures" --> EQ3
    D8 -- "secures" --> RE5
    D8 -. "high risk" .-> LS2
    D8 -- "secures (lien pos. 3)" --> EQ4
    
    %% Style definitions
    classDef loan fill:#ec4899,stroke:#d44087,color:white;
    classDef legal fill:#8b5cf6,stroke:#7349d1,color:white;
    classDef realEstate fill:#10b981,stroke:#09936a,color:white;
    classDef equipment fill:#38bdf8,stroke:#2da3db,color:white;
    classDef livestock fill:#a3e635,stroke:#85c11f,color:black;
    classDef account fill:#f59e0b,stroke:#d88a08,color:white;
    
    %% Apply styles
    class L1,L2,L3,L4,L5,L6 loan;
    class D1,D2,D3,D4,D5,D6,D7,D8 legal;
    class RE1,RE2,RE3,RE4,RE5 realEstate;
    class EQ1,EQ2,EQ3,EQ4 equipment;
    class LS1,LS2 livestock;
    class A1,A2 account;
```

## Data Model Relationship Overview

This diagram shows how different entities in the Farm Credit Collateral Management System relate to each other in a data model perspective, including the legal documents as intermediaries.

```mermaid
erDiagram
    ACCOUNT ||--o{ COLLATERAL : owns
    ACCOUNT ||--o{ LOAN : responsible_for
    ACCOUNT ||--o{ LEGAL_DOCUMENT : holds
    LOAN ||--o{ LEGAL_DOCUMENT : documents
    LEGAL_DOCUMENT }o--o{ COLLATERAL : secures
    COLLATERAL ||--o{ INSPECTION : undergoes
    COLLATERAL ||--o{ VALUATION : receives
    
    COLLATERAL {
        string id
        string name
        string type
        string subtype
        decimal value
        string size
        string location
        date last_appraisal
        string condition
    }
    
    LOAN {
        string id
        string name
        string type
        string subtype
        decimal amount
        date origination_date
        date maturity_date
        string status
    }
    
    ACCOUNT {
        string id
        string name
        string type
        string subtype
        string customer_id
        date relationship_since
        string contact
    }
    
    LEGAL_DOCUMENT {
        string id
        string name
        string type
        string document_type
        date execution_date
        date expiration_date
        string status
    }
    
    INSPECTION {
        string id
        date inspection_date
        string inspector
        string findings
        string recommendation
        string status
    }
    
    VALUATION {
        string id
        date valuation_date
        decimal market_value
        decimal net_realizable_value
        string appraiser
        string methodology
    }
```

## Loan Risk Assessment Flow

This diagram illustrates the different states a collateral item can go through in the risk assessment process, with the addition of legal document review.

```mermaid
stateDiagram-v2
    [*] --> Normal: Initial Assessment
    
    state "Risk Assessment" as RA
    Normal --> RA: Periodic Review
    
    state "Document Verification" as DV {
        CheckLegalDocuments --> ValidateStatus
        ValidateStatus --> CheckExpiration
        CheckExpiration --> IdentifyGaps
    }
    
    RA --> DV: Document Review Required
    
    state "Value Assessment" as VA {
        Appraisal --> MarketValue
        Appraisal --> NetRealizableValue
        MarketValue --> LNtoMVCalculation
        NetRealizableValue --> LNtoNRVCalculation
    }
    
    RA --> VA: Valuation Required
    DV --> VA: Documents Valid
    
    VA --> Normal: Acceptable Ratios
    VA --> HighRisk: LN/MV ratio > 75%
    VA --> Warning: Valuation outdated
    
    DV --> DocumentWarning: Expiring documents
    DV --> DocumentIssue: Invalid documents
    DocumentWarning --> DV: Documents renewed
    DocumentIssue --> DV: Documents corrected
    
    HighRisk --> Normal: Collateral value increases
    Warning --> Normal: Valuation updated
    HighRisk --> Warning: Valuation outdated
    Warning --> HighRisk: LN/MV ratio evaluated > 75% 
    
    Normal --> AdditionalCollateralRequired: LN/MV > 90%
    HighRisk --> AdditionalCollateralRequired: LN/MV > 90%
    
    AdditionalCollateralRequired --> Normal: Additional collateral secured
    
    Normal --> Foreclosure: Payment default > 90 days
    HighRisk --> Foreclosure: Payment default > 60 days
    Warning --> Foreclosure: Payment default > 90 days
    DocumentIssue --> Foreclosure: Documents invalidated
    
    Foreclosure --> LegalDocumentPreparation: Initiate proceedings
    LegalDocumentPreparation --> CollateralLiquidation: Legal proceedings complete
    CollateralLiquidation --> [*]: Collateral sold
