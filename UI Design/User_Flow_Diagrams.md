# Farm Credit Collateral Management System
## User Flow Diagrams

This document contains visual representations of the key user flows within the Farm Credit Collateral Management System. These diagrams help illustrate how users navigate through the system to complete their primary tasks.

## 1. Collateral Creation & Management Flow

```mermaid
flowchart TD
    A[Dashboard] -->|Click Create Collateral| B[Select Collateral Type]
    B --> C[Complete Basic Information]
    C --> D[Add Documentation/Attachments]
    D --> E[Set Valuation Method and Values]
    E --> F[Review and Submit]
    F --> G[Confirmation]
    G -->|Link to Loans| H[Select Loans for Linking]
    G -->|Edit| C
    G -->|Return to Dashboard| A
    H --> I[Set Lien Position]
    I --> J[Save Relationships]
    J --> K[View Web of Liability]
```

## 2. Loan-Collateral Relationship Management Flow

```mermaid
flowchart TD
    A[Dashboard] -->|Search| B[Search for Loan]
    B --> C[View Loan Details]
    C -->|Manage Collateral| D[View Current Relationships]
    D -->|Add Collateral| E[Search for Collateral]
    D -->|Remove Collateral| F[Select Collateral to Remove]
    D -->|Adjust Relationships| G[Modify Lien Positions]
    E --> H[Select Collateral from Results]
    H --> I[Set Lien Position/Allocation]
    F --> J[Confirm Removal]
    G --> K[Update Positions/Allocations]
    I --> L[Save Changes]
    J --> L
    K --> L
    L --> M[View Updated Web of Liability]
    M -->|Simulate Changes| N[Run What-If Scenarios]
    N --> O[View Simulation Results]
    O -->|Save Simulation| P[Name and Store Simulation]
    O -->|Discard| M
```

## 3. Risk Assessment Workflow

```mermaid
flowchart TD
    A[Dashboard] -->|Risk Assessment| B[Select Portfolio/Borrower]
    B --> C[View Risk Metrics]
    C -->|Drill Down| D[View Detailed Breakdown]
    D -->|Identify Concern| E[Flag for Review]
    D -->|Run Simulation| F[Set Simulation Parameters]
    F --> G[View Simulation Results]
    G -->|Adjust Parameters| F
    G -->|Save Findings| H[Document Observations]
    H --> I[Generate Risk Report]
    I -->|Share| J[Export/Email Report]
    I -->|Create Action Items| K[Assign Tasks]
    K --> A
```

## 4. Search & Reporting Flow

```mermaid
flowchart TD
    A[Any Screen] -->|Global Search| B[Enter Search Terms]
    B --> C[View Search Results]
    C -->|Filter Results| D[Apply Filters]
    D --> C
    C -->|Select Record| E[View Record Details]
    E -->|View Relationships| F[Open Web of Liability]
    E -->|Export Data| G[Select Export Format]
    G --> H[Download File]
    E -->|Generate Report| I[Select Report Template]
    I --> J[Customize Report Parameters]
    J --> K[Preview Report]
    K -->|Edit| J
    K -->|Generate| L[Download/Share Report]
    E -->|Save Search| M[Name and Save Search]
    M --> A
```

## 5. System Navigation Map

```mermaid
flowchart TD
    A[Login] --> B[Dashboard]
    B --> C[Collateral Management]
    B --> D[Loan Overview]
    B --> E[Risk Assessment]
    B --> F[Reports & Analytics]
    B --> G[Administration]
    
    C --> C1[Create Collateral]
    C --> C2[Search Collateral]
    C --> C3[Manage Valuations]
    C --> C4[Collateral Documents]
    
    D --> D1[Loan Search]
    D --> D2[Link Collateral]
    D --> D3[Loan Relationships]
    
    E --> E1[Portfolio Review]
    E --> E2[Simulation Tools]
    E --> E3[Risk Metrics]
    
    F --> F1[Standard Reports]
    F --> F2[Custom Reports]
    F --> F3[Data Export]
    
    G --> G1[User Management]
    G --> G2[System Configuration]
    G --> G3[Audit Logs]
```

## 6. Component Interaction Diagram

```mermaid
flowchart TD
    A[User Interface] <-->|API Calls| B[API Gateway]
    B <-->|Authentication| C[Identity Service]
    B <-->|Data Access| D[Data Services]
    D <-->|Read/Write| E[Database]
    D <-->|Integration| F[Existing Loan Systems]
    B <-->|Business Logic| G[Application Services]
    G <-->|Calculation| H[Risk Engine]
    G <-->|Storage| I[Document Store]
    A <-->|Real-time Updates| J[WebSocket Service]
    J <-->|Events| G
```

## 7. Responsive Design Adaptation Flow

```mermaid
flowchart TD
    A[User Device Detection] --> B{Device Type?}
    B -->|Desktop| C[Full Layout]
    B -->|Tablet| D[Adapted Layout]
    B -->|Mobile| E[Mobile Layout]
    
    C --> C1[Side Navigation]
    C --> C2[Multi-Column Views]
    C --> C3[Advanced Visualizations]
    
    D --> D1[Collapsible Navigation]
    D --> D2[Reduced Columns]
    D --> D3[Simplified Visualizations]
    
    E --> E1[Bottom Navigation]
    E --> E2[Single Column]
    E --> E3[Progressive Disclosure]
    
    C1 & C2 & C3 & D1 & D2 & D3 & E1 & E2 & E3 --> F[Content Adaptation]
    F --> G[Load Appropriate Components]
    G --> H[Render UI]
```

## 8. Web of Liability Node Interaction

```mermaid
flowchart TD
    A[Web of Liability View] --> B[Node Selection]
    B --> C{Node Type?}
    
    C -->|Loan| D[View Loan Details]
    C -->|Collateral| E[View Collateral Details]
    C -->|Account| F[View Account Details]
    C -->|Document| G[View Document Details]
    
    D & E & F & G --> H[View Related Nodes]
    H --> I[Secondary Selection]
    I --> J[Compare Relationship]
    
    B -->|Edge Selection| K[View Relationship Details]
    K --> L[Edit Relationship]
    L --> M[Update Graph]
    
    B -->|Multi-Select| N[Batch Actions]
    N --> O[Compare Selected]
    N --> P[Generate Report]
