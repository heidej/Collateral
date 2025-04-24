# Web of Liability Entity Relationships

This diagram illustrates the relationship structure between loans, collateral, and accounts in the Farm Credit Collateral Management System.

```mermaid
flowchart LR
    subgraph Loans
        L1["LC-2023-045\nLong Term"]
        L2["LC-2023-046\nIntermediate Term"]
        L3["LC-2023-089\nShort Term"]
        L4["LC-2024-012\nLong Term"]
        L5["LC-2024-025\nIntermediate Term"]
        L6["LC-2024-037\nOperating"]
    end

    subgraph "Real Estate"
        RE1["Farm Land - North\n120 Acres"]
        RE2["Farm Land - South\n85 Acres"]
        RE3["Orchard - West\n40 Acres"]
        RE4["Storage Facility\n12,000 sq ft"]
        RE5["Residential Property\nFarmhouse"]
    end

    subgraph Accounts
        A1["Smith Family Farms\nCustomer ID: 1024789"]
        A2["Smith Agricultural LLC\nCustomer ID: 1024790"]
    end
    
    subgraph "Equipment & Livestock"
        EQ1["Tractors (3)\n$175,000"]
        EQ2["Harvester\n$225,000"]
        EQ3["Irrigation System\n$80,000"]
        LS1["Dairy Cattle\n125 Head"]
        LS2["Poultry\n2,500 Birds"]
        EQ4["Farm Vehicles\n$95,000"]
    end
    
    %% Smith Family Farms relationships
    A1 --> RE1
    A1 --> RE2
    A1 --> RE3
    A1 --> EQ1
    A1 --> EQ2
    A1 --> LS1
    
    %% Smith Agricultural LLC relationships
    A2 --> RE4
    A2 --> RE5
    A2 --> EQ3
    A2 --> LS2
    A2 --> EQ4
    
    %% Loan to collateral relationships - high risk connections with dotted lines
    L1 -. "High Risk\n$350,000" .-> RE1
    L2 -- "$125,000" --> RE2
    L2 -- "$95,000" --> EQ1
    L3 -- "$75,000" --> LS1
    L4 -. "High Risk\n$280,000" .-> RE3
    L4 -- "$150,000" --> EQ2
    L5 -- "$110,000" --> RE4
    L5 -- "$65,000" --> EQ3
    L6 -- "$90,000" --> RE5
    L6 -. "High Risk\n$120,000" .-> LS2
    L6 -- "$45,000" --> EQ4
    
    %% Style definitions
    classDef loan fill:#4A90E2,stroke:#3A7CBF,color:white;
    classDef realEstate fill:#7ED321,stroke:#5FA919,color:white;
    classDef equipment fill:#50E3C2,stroke:#41B49B,color:white;
    classDef livestock fill:#F8E71C,stroke:#C6B916,color:black;
    classDef account fill:#F5A623,stroke:#E09600,color:white;
    
    %% Apply styles
    class L1,L2,L3,L4,L5,L6 loan;
    class RE1,RE2,RE3,RE4,RE5 realEstate;
    class EQ1,EQ2,EQ3,EQ4 equipment;
    class LS1,LS2 livestock;
    class A1,A2 account;
```

## Data Model Relationship Overview

This diagram shows how different entities in the Farm Credit Collateral Management System relate to each other in a data model perspective.

```mermaid
erDiagram
    ACCOUNT ||--o{ COLLATERAL : owns
    ACCOUNT ||--o{ LOAN : responsible_for
    LOAN }o--o{ COLLATERAL : secured_by
    COLLATERAL ||--o{ DOCUMENT : has
    COLLATERAL ||--o{ INSPECTION : undergoes
    COLLATERAL ||--o{ VALUATION : receives
    
    COLLATERAL {
        int id
        string name
        string type
        decimal value
        date last_updated
        string status
        string location
        decimal acreage
        string condition
    }
    
    LOAN {
        int id
        string loan_number
        string type
        decimal amount
        decimal ln_mv_ratio
        decimal ln_nrv_ratio
        date origination_date
        date maturity_date
        string status
        decimal interest_rate
    }
    
    ACCOUNT {
        int id
        string customer_id
        string name
        string type
        date relationship_since
        string status
        string contact_info
        string credit_score
    }
    
    DOCUMENT {
        int id
        string type
        string filename
        date uploaded
        string status
        string version
    }
    
    INSPECTION {
        int id
        date inspection_date
        string inspector
        string findings
        string recommendation
        string status
    }
    
    VALUATION {
        int id
        date valuation_date
        decimal market_value
        decimal net_realizable_value
        string appraiser
        string methodology
    }
```

## Loan Risk Assessment Flow

This diagram illustrates the different states a collateral item can go through in the risk assessment process.

```mermaid
stateDiagram-v2
    [*] --> Normal: Initial Assessment
    
    state "Risk Assessment" as RA
    Normal --> RA: Periodic Review
    
    state "Value Assessment" as VA {
        Appraisal --> MarketValue
        Appraisal --> NetRealizableValue
        MarketValue --> LNtoMVCalculation
        NetRealizableValue --> LNtoNRVCalculation
    }
    
    RA --> VA: Valuation Required
    
    VA --> Normal: Acceptable Ratios
    VA --> HighRisk: LN/MV ratio > 75%
    VA --> Warning: Valuation outdated
    
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
    
    Foreclosure --> CollateralLiquidation: Legal proceedings complete
    CollateralLiquidation --> [*]: Collateral sold
