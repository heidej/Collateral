# Farm Credit Collateral Management System
# Product Requirements Document (PRD)

## Document Information
**Document Title:** Farm Credit Collateral Management System PRD  
**Version:** 1.0  
**Date Created:** March 11, 2025  
**Status:** Draft  

## Table of Contents
1. [Introduction](#1-introduction)
2. [Product Overview](#2-product-overview)
3. [User Personas](#3-user-personas)
4. [User Requirements](#4-user-requirements)
5. [Functional Requirements](#5-functional-requirements)
6. [Non-Functional Requirements](#6-non-functional-requirements)
7. [UI/UX Requirements](#7-uiux-requirements)
8. [Technical Requirements](#8-technical-requirements)
9. [Implementation Phases](#9-implementation-phases)
10. [Release Criteria](#10-release-criteria)
11. [Assumptions and Constraints](#11-assumptions-and-constraints)
12. [Glossary](#12-glossary)

---

## 1. Introduction

### 1.1 Purpose
This Product Requirements Document (PRD) defines the requirements for the Farm Credit Collateral Management System. It provides a detailed description of the system's functionality, user interface, performance expectations, and implementation considerations to guide the development team.

### 1.2 Scope
The Farm Credit Collateral Management System will provide comprehensive collateral management capabilities for Farm Credit associations, enabling them to create, track, value, and manage relationships between collateral and loans. The system will integrate with existing loan management systems while providing enhanced visualization, reporting, and risk assessment capabilities.

### 1.3 Background
Farm Credit associations currently manage collateral through various systems with limited integration and visualization capabilities. The new system aims to consolidate collateral management into a modern, user-friendly platform that enhances operational efficiency and risk management.

---

## 2. Product Overview

### 2.1 Product Vision
Create a centralized, intuitive collateral management system that provides Farm Credit associations with comprehensive tools for managing and visualizing collateral relationships, valuations, and risk metrics.

### 2.2 Product Goals
1. Streamline collateral creation, valuation, and management
2. Provide clear visualization of complex collateral-loan relationships
3. Enhance risk assessment through improved calculations and reporting
4. Integrate seamlessly with existing Farm Credit systems
5. Maintain high data quality through validation and audit trails
6. Ensure security and compliance with Farm Credit standards
7. Reduce technical debt through modern architecture

### 2.3 Success Metrics
1. Reduction in time to create and manage collateral records
2. Improved accuracy in loan-to-value calculations
3. Increased user satisfaction with collateral management process
4. Decreased error rates in collateral data
5. Reduction in duplicate collateral records

---

## 3. User Personas

### 3.1 Primary Users
1. **Collateral Specialists**
   - Responsible for creating and managing collateral records
   - Need to link collateral to loans and perform valuations
   - Require clear visualization of relationships and dependencies

2. **Loan Officers**
   - Review collateral information related to loans
   - Need read-only access to collateral data
   - Require reports on collateral-to-loan ratios

3. **Credit Analysts**
   - Evaluate risk based on collateral portfolios
   - Need access to valuation methodologies and history
   - Require analytical tools for portfolio assessment

4. **System Administrators**
   - Configure system settings and user access
   - Manage integrations with external systems
   - Monitor system performance and usage

### 3.2 Secondary Users
1. **Executives and Managers**
   - Review portfolio-level reports and metrics
   - Need dashboard views of collateral performance

2. **Compliance Officers**
   - Ensure adherence to regulatory requirements
   - Review audit trails and data validation records

3. **IT Support Staff**
   - Troubleshoot system issues
   - Support integrations with other systems

---

## 4. User Requirements

### 4.1 Collateral Creation and Management
- Users must be able to create new collateral records with all required fields
- Users must be able to edit existing collateral records
- Users must be able to search for collateral using various criteria
- Users must be able to link collateral to loan records

### 4.2 Visualization and Relationships
- Users must be able to view a Web of Liability visualization showing relationships between collateral, loans, and accounts
- Users must be able to view relationship maps between properties, owners, and legal documents
- Users must be able to simulate changes to collateral allocations

### 4.3 Valuation and Risk Assessment
- Users must be able to record and calculate valuations using multiple methodologies
- Users must be able to configure and apply Net Realizable Value (NRV) rules
- Users must be able to view loan-to-value calculations based on both actual value and NRV

### 4.4 Reporting
- Users must be able to generate internal reports on collateral
- Users must be able to export data for external reporting

### 4.5 Integration
- Users must be able to view loan and account information from existing systems
- Users must have confidence that changes in integrated systems are reflected promptly

---

## 5. Functional Requirements

### 5.1 Collateral Record Management

#### 5.1.1 Collateral Creation and Editing
- **Description:** Allow users to create new collateral records and edit existing ones with a comprehensive set of fields for property details, valuation information, and other attributes.
- **Acceptance Criteria:**
  - System provides a form interface for creating collateral records
  - All required fields are validated before submission
  - Existing records can be edited with changes tracked
  - Attachments (documents, images) can be uploaded and associated with collateral
- **Priority:** MVP Features (Must Have)

#### 5.1.2 Read-Only Loan and Account Display
- **Description:** Display loan and account information from existing systems while preventing users from modifying this data directly.
- **Acceptance Criteria:**
  - Loan data is displayed in a read-only format
  - Integration with existing loan systems is seamless
  - All relevant loan details are visible to authorized users
- **Priority:** MVP Features (Must Have)

#### 5.1.3 Collateral Search & Retrieval
- **Description:** Provide advanced search capabilities to find collateral records based on various criteria such as property address, borrower name, collateral type, etc.
- **Acceptance Criteria:**
  - Search functionality supports multiple criteria
  - Results can be filtered and sorted
  - Search is performant even with large datasets
  - Most recently accessed records are easily accessible
- **Priority:** MVP Features (Must Have)

### 5.2 Loan-Collateral Relationship Management

#### 5.2.1 Collateral-Loan Linking
- **Description:** Enable users to link collateral records to loan records, capturing key information such as lien position and "Abundance of Caution" status.
- **Acceptance Criteria:**
  - Users can link multiple collateral items to a loan
  - Users can specify lien position for each collateral-loan link
  - Users can mark collateral as "Abundance of Caution"
  - Links can be modified or removed by authorized users
- **Priority:** MVP Features (Must Have)

#### 5.2.2 Web of Liability Visualization
- **Description:** Provide an interactive visualization showing how collateral items are connected to loans and accounts, helping users understand complex liability relationships.
- **Acceptance Criteria:**
  - Visualization shows all relationships between collateral, loans, and accounts
  - Users can interact with visualization to explore relationships
  - Visualization is performant with complex relationship networks
  - Critical for supporting calculations
- **Priority:** MVP Features (Must Have)

#### 5.2.3 Visual Relationship Mapping
- **Description:** Provide clear visual representation of relationships between properties, owners, and legal documents.
- **Acceptance Criteria:**
  - Visualization shows property-owner-document relationships
  - Users can navigate through relationship maps intuitively
  - Visualizations support UX enhancement goals
- **Priority:** MVP Features (Must Have)

#### 5.2.4 Collateral Allocation Simulation
- **Description:** Allow users to simulate changes to collateral allocations and see the impact on loan-to-value ratios and other risk metrics.
- **Acceptance Criteria:**
  - Users can create simulation scenarios without affecting live data
  - System calculates impact on LTV and other metrics in real-time
  - Multiple scenarios can be compared
  - Simulations can be saved or discarded
- **Priority:** MVP Features (Must Have)

### 5.3 Valuation and Risk Assessment

#### 5.3.1 Multi-Method Appraisal Support
- **Description:** Support multiple appraisal methodologies including comparable market valuation, benchmark per acre valuations, and income-based methodologies.
- **Acceptance Criteria:**
  - System supports all required appraisal methodologies
  - Users can select appropriate methodology based on collateral type
  - All calculations are performed accurately
  - Historical valuation data is preserved
- **Priority:** MVP Features (Must Have)

#### 5.3.2 Customizable NRV Rules
- **Description:** Allow associations to define custom Net Realizable Value (NRV) rules based on collateral type, lien position, and whether prior lien holder is Farm Credit or an outside lender.
- **Acceptance Criteria:**
  - Associations can configure NRV rules through an admin interface
  - Rules can be based on multiple criteria
  - Rules are properly applied in calculations
  - Changes to rules are tracked for audit purposes
- **Priority:** MVP Features (Must Have)

#### 5.3.3 Loan-to-Value Calculation
- **Description:** Automatically calculate and display Loan-to-Value ratios based on both Actual Value and Net Realizable Value.
- **Acceptance Criteria:**
  - Calculations include allocation percentages
  - Results match calculations from legacy systems
  - Calculations are performed in real-time
  - History of calculations is preserved
- **Priority:** MVP Features (Must Have)

#### 5.3.4 Collateral Benchmarking
- **Description:** Provide benchmarking capabilities to compare collateral valuations against market trends and similar properties.
- **Acceptance Criteria:**
  - System can compare valuations against benchmarks
  - Illinois-specific benchmarking functionality is provided
  - Benchmarks are regularly updated
  - Variance from benchmarks is clearly displayed
- **Priority:** Near Term (Nice to Have), Required for Illinois go-live

### 5.4 GIS and Spatial Features

#### 5.4.1 GIS Data Integration
- **Description:** Capture and store GIS data such as census tract, flood zone, water district, and GPS coordinates for collateral properties.
- **Acceptance Criteria:**
  - GIS data fields are available for collateral records
  - Integration with external GIS data sources is supported
  - Data is validated for accuracy
- **Priority:** Near Term (Nice to Have)

#### 5.4.2 Map Visualization and Overlays
- **Description:** Display collateral on interactive maps with various overlay options (flood zones, water districts, etc.) to visualize geographical relationships and risks.
- **Acceptance Criteria:**
  - Interactive map shows collateral locations
  - Multiple overlay options are available
  - Map is performant even with many data points
  - Users can zoom and filter map data
- **Priority:** Near Term (Nice to Have)

#### 5.4.3 Region Concentration Analysis
- **Description:** Analyze and visualize concentration of collateral and loans by geographical region to identify risk exposure.
- **Acceptance Criteria:**
  - System can generate heat maps of collateral concentration
  - Reports show concentration metrics by region
  - Alerts for high concentration can be configured
- **Priority:** Backlog (Future Release)

### 5.5 Reporting and Documentation

#### 5.5.1 Internal Reporting
- **Description:** Generate comprehensive internal reports including detailed valuation methodologies and risk metrics not shown to customers.
- **Acceptance Criteria:**
  - Standard report templates are available
  - Reports can be customized by users
  - Export to multiple formats is supported
  - Reports include all required data fields
- **Priority:** MVP Features (Must Have)

#### 5.5.2 External Reporting
- **Description:** Create customer-facing reports with appropriate formatting and content filtering to exclude internal-only information.
- **Acceptance Criteria:**
  - External reports filter sensitive internal data
  - Reports have professional formatting
  - Reports can be customized by associations
- **Priority:** Near Term (Nice to Have)

#### 5.5.3 Property Tax and Escrow Integration
- **Description:** Import and manage property tax information with integration to escrow reporting systems.
- **Acceptance Criteria:**
  - Property tax data can be imported and stored
  - Integration with escrow systems is supported
  - Tax payment status is tracked
- **Priority:** Backlog (Future Release)

### 5.6 Workflow Automation

#### 5.6.1 Appraisal Update Workflow
- **Description:** Enable users to generate appraisal update requests and track them through a defined workflow process.
- **Acceptance Criteria:**
  - Workflow supports appraisal update process
  - Status tracking is available
  - Notifications are sent at key workflow points
  - Note: May not be needed if managed in nCino/Salesforce
- **Priority:** Long Term (Nice to Have)

#### 5.6.2 Portfolio Valuation Updates
- **Description:** Allow authorized users to apply benchmark valuation updates across multiple collateral properties, automatically updating derived calculations.
- **Acceptance Criteria:**
  - Batch updates can be applied to multiple properties
  - All derived calculations (L/AV, L/NRV, LGD) are updated
  - Updates are logged for audit purposes
  - Only authorized users can perform batch updates
- **Priority:** Long Term (Nice to Have)

#### 5.6.3 Portfolio Efficiency Analysis
- **Description:** Provide tools for analyzing efficiency and bottlenecks in collateral updates, time to market, accuracy, etc.
- **Acceptance Criteria:**
  - System tracks metrics on collateral management processes
  - Dashboards show efficiency metrics
  - Bottlenecks can be identified and analyzed
- **Priority:** Backlog (Future Release)

### 5.7 AI and Agent Integration

#### 5.7.1 Data Validation Agent
- **Description:** Implement an AI agent to validate data entry, identify potential errors, and ensure data quality across the system.
- **Acceptance Criteria:**
  - AI identifies data entry errors in real-time
  - Suggestions for corrections are provided
  - Quality metrics are tracked and reported
- **Priority:** Near Term (Nice to Have)

#### 5.7.2 Valuation Suggestion Agent
- **Description:** Provide AI-driven suggestions for property valuations based on comparable properties, market trends, and historical data.
- **Acceptance Criteria:**
  - AI suggests valuations based on comparable properties
  - Suggestions include confidence levels
  - Users can accept or modify suggestions
  - Note: Some associations may use third-party applications
- **Priority:** Long Term (Nice to Have)

#### 5.7.3 Document Parsing Agent
- **Description:** Use AI to extract relevant information from uploaded documents (appraisals, legal descriptions, etc.) to reduce manual data entry.
- **Acceptance Criteria:**
  - AI extracts key data points from documents
  - Accuracy metrics are provided
  - Users can verify and correct extracted data
- **Priority:** Long Term (Nice to Have)

#### 5.7.4 Lien Position Optimizer Agent
- **Description:** Recommend optimal lien positions based on association rules, existing loans, and whether the prior lien holder is a Farm Credit entity or external lender.
- **Acceptance Criteria:**
  - AI recommends optimal lien positions
  - Recommendations consider all relevant factors
  - Users can accept or modify recommendations
- **Priority:** Backlog (Future Release)

#### 5.7.5 Risk Assessment Agent
- **Description:** Analyze collateral portfolio to identify potential risks, such as concentration risk, valuation outliers, or compliance issues.
- **Acceptance Criteria:**
  - AI identifies potential risk factors
  - Risk reports include mitigation suggestions
  - Alerts for high-risk situations can be configured
- **Priority:** Backlog (Future Release)

### 5.8 Visualization and User Experience

#### 5.8.1 Automatic Save Functionality
- **Description:** Implement automatic saving of data with visual indicators to prevent data loss and improve user experience.
- **Acceptance Criteria:**
  - Data is saved automatically at regular intervals
  - Visual indicators show save status
  - Users can manually save at any time
  - Recovery options are available for unsaved changes
- **Priority:** MVP Features (Must Have)

#### 5.8.2 Customer Search Optimization
- **Description:** Enhance customer search capabilities with filters, auto-complete, and quick access to frequently used records.
- **Acceptance Criteria:**
  - Search includes auto-complete functionality
  - Recently accessed records are easily available
  - Search results load quickly
  - Filters can be applied to search results
- **Priority:** MVP Features (Must Have)

#### 5.8.3 Data Wizards for Entry
- **Description:** Create guided data entry wizards for collateral objects to ensure complete and accurate information.
- **Acceptance Criteria:**
  - Step-by-step wizards guide users through data entry
  - Validation occurs at each step
  - Progress is saved between steps
  - Users can navigate back and forth between steps
- **Priority:** Near Term (Nice to Have)

### 5.9 Integration and Interoperability

#### 5.9.1 Legacy System Integration
- **Description:** Implement secure APIs or data connectors to integrate with existing loan and account management systems.
- **Acceptance Criteria:**
  - Seamless integration with legacy systems
  - Data integrity is maintained across systems
  - Performance meets requirements even during peak loads
  - Error handling and recovery procedures are in place
- **Priority:** MVP Features (Must Have)

#### 5.9.2 External Data Source Integration
- **Description:** Connect to external data sources for property information, market data, flood maps, etc.
- **Acceptance Criteria:**
  - Integration with required external data sources
  - Data is validated and normalized
  - UCC Filing functionality is supported if required
- **Priority:** Near Term (Nice to Have)

#### 5.9.3 Real-Time Data Synchronization
- **Description:** Ensure that changes in integrated systems are reflected promptly in the collateral management system.
- **Acceptance Criteria:**
  - Unidirectional data flow (Collateral App receives in real-time, sends on demand)
  - Changes are reflected within acceptable time limits
  - Synchronization errors are logged and resolved
  - Notification of failed synchronization events
- **Priority:** MVP Features (Must Have)

### 5.10 Security and Compliance

#### 5.10.1 Role-Based Access Control
- **Description:** Implement fine-grained access controls to ensure users can only perform actions appropriate to their role.
- **Acceptance Criteria:**
  - Roles can be defined with specific permissions
  - Users can be assigned to multiple roles
  - Access is restricted based on role permissions
  - Permission changes take effect immediately
- **Priority:** MVP Features (Must Have)

#### 5.10.2 Audit Trail
- **Description:** Maintain comprehensive logs of all system actions for compliance and troubleshooting purposes.
- **Acceptance Criteria:**
  - All significant actions are logged with timestamp and user
  - Audit logs cannot be modified
  - Logs can be searched and filtered
  - Reports can be generated from audit logs
- **Priority:** MVP Features (Must Have)

#### 5.10.3 Data Validation Rules
- **Description:** Enforce data quality through validation rules that prevent incorrect or incomplete information.
- **Acceptance Criteria:**
  - Comprehensive validation rules for all data fields
  - Real-time validation during data entry
  - Batch validation for imported data
  - Clear error messages for validation failures
- **Priority:** MVP Features (Must Have)

---

## 6. Non-Functional Requirements

### 6.1 Performance Requirements
1. **Response Time:** The system must respond to user interactions within 2 seconds under normal load conditions.
2. **Concurrent Users:** The system must support at least 100 concurrent users without degradation in performance.
3. **Scalability:** The system architecture must allow for scaling to accommodate future growth in users and data volume.
4. **Batch Processing:** Batch processes must complete within defined timeframes, with larger operations scheduled during off-peak hours.

### 6.2 Security Requirements
1. **Authentication:** The system must authenticate users through secure methods compatible with existing Farm Credit systems.
2. **Authorization:** The system must enforce role-based access controls for all functions.
3. **Data Encryption:** All sensitive data must be encrypted both in transit and at rest.
4. **Security Compliance:** The system must comply with Farm Credit security policies and relevant regulations.
5. **Vulnerability Management:** Regular security assessments must be conducted, and vulnerabilities addressed promptly.

### 6.3 Reliability and Availability
1. **Uptime:** The system must maintain 99.9% uptime during business hours.
2. **Backup and Recovery:** Regular backups must be performed, with defined recovery procedures and targets.
3. **Fault Tolerance:** The system must be designed to handle component failures without complete system failure.
4. **Error Handling:** The system must provide clear error messages and recovery paths for all error conditions.

### 6.4 Usability Requirements
1. **User Interface:** The system must provide an intuitive, modern user interface that requires minimal training.
2. **Accessibility:** The system must comply with accessibility standards, including WCAG 2.1 AA.
3. **Documentation:** Comprehensive user documentation must be provided, including contextual help within the application.
4. **Consistency:** The user interface must maintain consistent design patterns throughout the application.

### 6.5 Maintainability and Support
1. **Supportability:** The system must include monitoring and diagnostic tools to facilitate support.
2. **Code Quality:** The codebase must follow established coding standards and best practices.
3. **Documentation:** Technical documentation must be maintained, including architecture, design decisions, and API specifications.
4. **Upgrades:** The system must support upgrading components without significant downtime.

### 6.6 Compatibility
1. **Browser Compatibility:** The system must function correctly on the latest versions of major browsers (Chrome, Firefox, Edge, Safari).
2. **Device Compatibility:** The system must be responsive and functional on desktop and tablet devices.
3. **Integration Compatibility:** The system must integrate with specified versions of existing Farm Credit systems.

### 6.7 Compliance
1. **Regulatory Compliance:** The system must comply with relevant regulatory requirements for financial institutions.
2. **Audit Support:** The system must provide tools and reports to facilitate internal and external audits.
3. **Data Retention:** The system must support data retention policies as defined by Farm Credit governance.

---

## 7. UI/UX Requirements

### 7.1 Design Principles
1. The user interface should be clean, modern, and intuitive.
2. The design should prioritize usability and efficiency for frequent tasks.
3. Visualizations should be clear and interactive, providing insights at a glance.
4. The interface should be responsive to different screen sizes and devices.

### 7.2 Key UI Components
1. **Dashboard:** Personalized dashboard showing key metrics and recently accessed records.
2. **Collateral Management Interface:** Forms and tools for creating and managing collateral records.
3. **Visualization Tools:** Interactive displays for Web of Liability and relationship mapping.
4. **Search Interface:** Advanced search capabilities with filters and saved searches.
5. **Reporting Interface:** Tools for generating and customizing reports.

### 7.3 User Workflow Optimization
1. Common tasks should be accessible with minimal clicks.
2. Data entry should be streamlined with auto-save and validation.
3. Related information should be logically grouped and easily accessible.
4. Navigation should be intuitive and consistent throughout the application.

### 7.4 Feedback and Interaction
1. The system should provide clear visual feedback for user actions.
2. Error messages should be descriptive and suggest corrective actions.
3. Success confirmations should be provided for important actions.
4. Progress indicators should be displayed for longer operations.

---

## 8. Technical Requirements

### 8.1 Architecture
1. The system should be built on a modern, service-oriented architecture.
2. Components should be modular and loosely coupled to facilitate maintenance and scaling.
3. The architecture should support integration with existing Farm Credit systems.

### 8.2 Data Management
1. The data model should be extensible to accommodate future requirements.
2. Data integrity constraints should be enforced at the database level where appropriate.
3. Historical data should be preserved for audit and analysis purposes.
4. The system should include data migration tools for importing existing collateral data.

### 8.3 APIs and Integration
1. The system should provide RESTful APIs for integration with other systems.
2. API authentication and authorization should follow security best practices.
3. API versioning should be supported to facilitate future changes.
4. Integration with specified external systems should be implemented using appropriate technologies.

### 8.4 AI Agents
1. The system should utilize AI Agents to enhance user productivity and data quality.
2. Agent implementation should follow a standardized framework for consistency.
3. Agents should be designed with clear boundaries of responsibility and authority.
4. Agent behaviors should be configurable by system administrators.
5. Agent actions should be logged and traceable for audit purposes.
6. All agent interactions should follow established security protocols.
7. Agent performance should be monitored and optimized over time.
8. Initial agent implementations should focus on:
   - Data Validation Agent
   - Valuation Suggestion Agent
   - Document Parsing Agent
9. Future agent implementations should include:
   - Lien Position Optimizer Agent
   - Risk Assessment Agent

### 8.5 Logging and Monitoring
1. The system should log all significant events for troubleshooting and audit purposes.
2. Performance metrics should be collected and available for analysis.
3. Alerts should be configured for critical system events and performance thresholds.
4. Log retention policies should comply with Farm Credit requirements.

---

## 9. Implementation Phases

### 9.1 MVP Features
1. **Collateral Creation and Editing**
2. **Read-Only Loan and Account Display**
3. **Collateral Search & Retrieval**
4. **Collateral-Loan Linking**
5. **Web of Liability Visualization**
6. **Visual Relationship Mapping**
7. **Collateral Allocation Simulation**
8. **Multi-Method Appraisal Support**
9. **Customizable NRV Rules**
10. **Loan-to-Value Calculation**
11. **Internal Reporting**
12. **Automatic Save Functionality**
13. **Customer Search Optimization**
14. **Legacy System Integration**
15. **Role-Based Access Control**
16. **Audit Trail**
17. **Data Validation Rules**
18. **Real-Time Data Synchronization**

### 9.2 Near Term Features
1. **Data Wizards for Entry**
2. **Collateral Benchmarking** (Required for Illinois go-live)
3. **GIS Data Integration**
4. **Map Visualization and Overlays**
5. **External Reporting**
6. **Data Validation Agent**
7. **External Data Source Integration**

### 9.3 Long Term Features
1. **Appraisal Update Workflow**
2. **Portfolio Valuation Updates**
3. **Valuation Suggestion Agent**
4. **Document Parsing Agent**

### 9.4 Future Backlog
1. **Region Concentration Analysis**
2. **Property Tax and Escrow Integration**
3. **Portfolio Efficiency Analysis**
4. **Risk Assessment Agent**
5. **Lien Position Optimizer Agent**

---

## 10. Release Criteria

### 10.1 MVP Release Criteria
1. All MVP features have been implemented and tested.
2. Performance requirements have been met under expected load.
3. Security testing has been completed with no critical or high vulnerabilities.
4. User acceptance testing has been completed with no critical issues.
5. System documentation is complete.
6. Support procedures and training materials are in place.

### 10.2 Near Term Release Criteria
1. All Near Term features have been implemented and tested.
2. Integration with GIS systems has been verified.
3. Illinois-specific requirements have been validated with stakeholders.
4. User acceptance testing has been completed with no critical issues.

### 10.3 Long Term Release Criteria
1. All Long Term features have been implemented and tested.
2. AI-based features have been validated for accuracy and performance.
3. Workflow automation has been tested end-to-end.
4. User acceptance testing has been completed with no critical issues.

---

## 11. Assumptions and Constraints

### 11.1 Assumptions
1. Legacy systems will remain available and provide necessary APIs for integration.
2. Farm Credit associations will provide subject matter experts for requirements validation and testing.
3. Data migration from existing systems will be a separate initiative with its own requirements.
4. Existing nCino/Salesforce workflows will remain the system of record for some processes.

### 11.2 Constraints
1. The system must integrate with existing Farm Credit infrastructure.
2. The system must comply with Farm Credit security policies and regulatory requirements.
3. Implementation priorities may be influenced by association-specific needs (e.g., Illinois requirements).
4. Changes to the system will need to be evaluated for impact on FPI partner systems.

### 11.3 Dependencies
1. Changes to Financial Services Cloud (Salesforce) projects to use the new system.
2. Availability of APIs and data from integrated systems.
3. Coordination with other Farm Credit technology initiatives.

### 11.4 Implementation Considerations
1. Evaluate the impact of changeover on existing FPI partner systems.
2. Financial Services Cloud (Salesforce) projects will need to be updated to use the new system.
3. Determine whether updates occur during Salesforce go-live or after.
4. Ensure configurability for different Farm Credit associations.
5. Focus on intuitive interfaces, especially for complex visualizations.
6. Optimize performance for large portfolios and complex calculations.
7. Provide comprehensive training and documentation.
8. Leverage modern technologies to avoid creating new technical debt.

---

## 12. Glossary

**Abundance of Caution**: Collateral taken as an extra precaution even though the loan might be adequately secured by other collateral.

**Collateral**: Assets pledged by a borrower to secure a loan.

**Lien Position**: The order in which creditors have claims on the collateral in case of default.

**Loan-to-Value (LTV)**: The ratio of the loan amount to the value of the asset secured by the loan.

**Net Realizable Value (NRV)**: The estimated selling price of an asset in the ordinary course of business, less estimated costs of completion and disposal.

**UCC Filing**: A legal form filed with a state government that announces a creditor's interest in a debtor's property.

**Web of Liability**: A visual representation showing how collateral items are connected to loans and accounts.

**GIS (Geographic Information System)**: A system designed to capture, store, manipulate, analyze, manage, and present spatial or geographic data.

**API (Application Programming Interface)**: A set of definitions and protocols for building and integrating application software.

**nCino**: A cloud-based bank operating system built on the Salesforce platform.

**Salesforce**: A customer relationship management platform used by Farm Credit associations.

**FPI (Farm Production & IT)**: Partner systems that integrate with the Farm Credit Collateral Management System.
