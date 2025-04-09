# Farm Credit Collateral Management System
# PRD Visualizations

This document contains the visual representations of the system architecture, user flows, and relationship models for the Farm Credit Collateral Management System using Mermaid diagrams.

## System Architecture

```mermaid
graph TD
    User[User/Browser] --> |HTTP/HTTPS| WebApp[Web Application]
    WebApp --> |API| BE[Backend Services]
    BE --> |Query/Update| DB[(Database)]
    BE --> |Integration| LoanSys[Loan Management System]
    BE --> |Integration| CustSys[Customer Management System]
    BE --> |Integration| DocSys[Document Management System]
    BE --> |Service| Calc[Calculation Engine]
    BE --> |Service| Viz[Visualization Engine]
    BE --> |Service| AI[AI/ML Services]
    BE --> |Service| Report[Reporting Engine]
    
    subgraph "Client Layer"
        User
        WebApp
    end
    
    subgraph "Services Layer"
        BE
        Calc
        Viz
        AI
        Report
    end
    
    subgraph "Data Layer"
        DB
    end
    
    subgraph "Integration Layer"
        LoanSys
        CustSys
        DocSys
    end
```

## User Workflow - Collateral Creation

```mermaid
sequenceDiagram
    actor User
    participant Home as Home Page
    participant Search as Search Feature
    participant Canvas as Collateral Canvas
    participant Wizard as Data Wizard
    participant DB as Database
    
    User->>Home: Navigate to Home Page
    User->>Search: Search for Customer
    Search->>DB: Query Customer Data
    DB-->>Search: Return Customer Results
    User->>Search: Select Customer
    Search->>Canvas: Load Customer Collateral Canvas
    User->>Canvas: Add New Collateral
    Canvas->>Wizard: Open Collateral Data Wizard
    User->>Wizard: Fill Required Panel 1 (Collateral Info)
    Wizard->>DB: Auto-Save on Panel Navigation
    User->>Wizard: Fill Required Panel 2 (Owners)
    Wizard->>DB: Auto-Save on Panel Navigation
    User->>Wizard: Fill Panel 3 (Appraisal Info)
    Wizard->>DB: Auto-Save on Panel Navigation
    User->>Wizard: Fill Panel 4 (if Real Estate)
    User->>Wizard: Submit
    Wizard->>DB: Save Collateral Record
    Wizard->>Canvas: Update Canvas with New Collateral
    Canvas-->>User: Display "Changes Saved" Indicator
```

## Web of Liability - Component Relationships

```mermaid
graph TD
    Customer[Customer] --> |Primary Borrower| Loan1[Loan 1 - ST]
    Customer --> |Co-Borrower| Loan2[Loan 2 - IT]
    Customer --> |Guarantor| Loan3[Loan 3 - LT]
    Customer --> |Owns| Coll1[Collateral 1]
    
    Loan1 --> |Secured By| SecDoc1[Security Document 1]
    Loan2 --> |Secured By| SecDoc2[Security Document 2]
    Loan3 --> |Secured By| SecDoc3[Security Document 3]
    
    SecDoc1 --> |Secures| Coll1
    SecDoc1 --> |Secures| Coll2[Collateral 2]
    SecDoc2 --> |Secures| Coll1
    SecDoc3 --> |Secures| Coll3[Collateral 3]
    
    Coll1 --> |Owned By| Customer
    Coll2 --> |Owned By| Cust2[Other Customer]
    Coll3 --> |Owned By| Customer
    
    subgraph "Short Term Loans"
        Loan1
    end
    
    subgraph "Intermediate Term Loans"
        Loan2
    end
    
    subgraph "Long Term Loans"
        Loan3
    end
    
    style Loan1 fill:#ff9999
    style Loan2 fill:#99ccff
    style Loan3 fill:#99ff99
    style Customer fill:#ffcc99
    style Coll1 fill:#cc99ff
    style Coll2 fill:#cc99ff
    style Coll3 fill:#cc99ff
    style SecDoc1 fill:#ffff99
    style SecDoc2 fill:#ffff99
    style SecDoc3 fill:#ffff99
```

## Collateral Data Model

```mermaid
erDiagram
    CUSTOMER ||--o{ LOAN : "is borrower on"
    CUSTOMER ||--o{ COLLATERAL : "owns"
    LOAN ||--o{ SECURITY_DOCUMENT : "secured by"
    SECURITY_DOCUMENT ||--o{ COLLATERAL : "secures"
    COLLATERAL ||--o{ COLLATERAL_DETAIL : "has"
    
    CUSTOMER {
        int customer_id PK
        string name
        string address
        string phone
        string tax_id
        int branch_id FK
    }
    
    LOAN {
        int loan_id PK
        int customer_id FK
        string loan_number
        string loan_name
        decimal loan_amount
        string loan_type
        date maturity_date
    }
    
    COLLATERAL {
        int collateral_id PK
        string collateral_type
        string description
        decimal market_value
        decimal nrv_percentage
        decimal prior_lien
    }
    
    SECURITY_DOCUMENT {
        int security_doc_id PK
        int loan_id FK
        string doc_type
        date doc_date
        string doc_number
    }
    
    COLLATERAL_DETAIL {
        int detail_id PK
        int collateral_id FK
        string detail_type
        string detail_value
    }
    
    SECURITY_DOC_COLLATERAL {
        int security_doc_id FK
        int collateral_id FK
        int lien_position
        boolean aoc_flag
    }
```

## User Interface Layout - Home Page

```mermaid
graph TD
    subgraph "Home Page Layout"
        Header[Header with Logo & Search Bar]
        Tabs[Navigation Tabs: Home, Collateral View, Collateral Analysis]
        MainArea[Main Content Area]
        Footer[Footer with Quick Analysis Link]
    end
    
    Header --> Tabs
    Tabs --> MainArea
    MainArea --> Footer
    
    subgraph "Main Content Area - Home"
        Search[Customer Search Box]
        RecentList[Recently Viewed Customers]
        QuickLinks[Quick Links]
    end
    
    subgraph "Main Content Area - Collateral View"
        Canvas[Collateral Visualization Canvas]
        Tools[Canvas Toolbox]
    end
    
    subgraph "Main Content Area - Collateral Analysis"
        Metrics[Key Metrics]
        DetailCalc[Detailed Calculations]
        Reports[Report Generation]
    end
```

## Collateral Wizard Workflow

```mermaid
stateDiagram-v2
    [*] --> Start
    Start --> Panel1: Create New Collateral
    
    state Panel1 {
        [*] --> CollType
        CollType --> Description
        Description --> MarketValue
        MarketValue --> NRVPercent
        NRVPercent --> PriorLien
        PriorLien --> [*]
    }
    
    state Panel2 {
        [*] --> Owner
        Owner --> PrimaryOwner
        PrimaryOwner --> PercentOwned
        PercentOwned --> [*]
    }
    
    state Panel3 {
        [*] --> Method
        Method --> Name
        Name --> Appraiser
        Appraiser --> Date
        Date --> Comments
        Comments --> [*]
    }
    
    state Panel4 {
        [*] --> Acres
        Acres --> Income
        Income --> Debt
        Debt --> [*]
    }
    
    Panel1 --> Panel2: Next
    Panel2 --> Panel3: Next
    Panel3 --> Panel4: Next (if Real Estate)
    Panel4 --> Submit: Next
    
    Panel2 --> Panel1: Back
    Panel3 --> Panel2: Back
    Panel4 --> Panel3: Back
    
    Submit --> Complete
    Complete --> [*]
    
    Panel1 --> Save: Continue Later
    Panel2 --> Save: Continue Later
    Panel3 --> Save: Continue Later
    Panel4 --> Save: Continue Later
    Save --> [*]
```

## Quick Loan Analysis Calculation Flow

```mermaid
flowchart TD
    start([Start]) --> input[Load Collateral & Loan Data]
    input --> proc1[Calculate Total Loan Amounts by Position]
    proc1 --> proc2[Calculate Allocation Percentage]
    proc2 --> proc3[Calculate Allocated Market Value]
    proc3 --> proc4[Calculate Final Adjusted NRV Amount]
    
    proc4 --> branch{For Each Loan}
    branch --> loanCalc1[Calculate Adjusted Loan Amount]
    loanCalc1 --> loanCalc2[Sum Allocated Market Values]
    loanCalc2 --> loanCalc3[Sum Final Adj. NRV Amounts]
    loanCalc3 --> loanCalc4[Calculate Loan/MV Ratio]
    loanCalc4 --> loanCalc5[Calculate Loan/NRV Ratio]
    loanCalc5 --> display[Display in Quick Analysis]
    
    display --> end1([End])
    
    subgraph "Collateral Calculations"
        proc1
        proc2
        proc3
        proc4
    end
    
    subgraph "Loan Calculations"
        loanCalc1
        loanCalc2
        loanCalc3
        loanCalc4
        loanCalc5
    end
```

## Implementation Phases Timeline

```mermaid
gantt
    title Farm Credit Collateral Management System Implementation
    dateFormat X
    axisFormat %d
    
    section Phase 1 - MVP
    Planning & Requirements      :a1, 0, 30d
    Core Collateral Management   :a2, after a1, 45d
    Basic Visualization          :a3, after a1, 45d
    Integration                  :a4, after a2, 30d
    User Management              :a5, after a2, 30d
    Testing & Bug Fixing         :a6, after a3 a4 a5, 30d
    
    section Phase 2 - Enhanced Features
    Advanced Visualization       :b1, after a6, 45d
    Reporting                    :b2, after a6, 45d
    Full Integration             :b3, after b1, 30d
    Audit Trail                  :b4, after b2, 30d
    Testing & Bug Fixing         :b5, after b3 b4, 30d
    
    section Phase 3 - AI and Analytics
    Data Validation Agent        :c1, after b5, 60d
    Valuation Assistance         :c2, after c1, 60d
    Advanced Analytics           :c3, after c2, 45d
    Mobile Access                :c4, after b5, 45d
    Testing & Bug Fixing         :c5, after c3 c4, 30d
```
