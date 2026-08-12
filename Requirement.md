# Requirement Document: PoC MCP Server for Bond Analysis

## 1. Objective

Develop a Proof of Concept (PoC) MCP (Model Context Protocol) server that integrates with an existing mock application to analyze investment grade corporate bonds.

The MCP server will ingest bond issuance data, process market terms such as IPT, NIC, oversubscription, coupon, redemption, and syndicate, and expose structured analytics as MCP-compliant context services for consumption by AI models and client applications.

## 2. Scope

### Data Ingestion

- Bond issuance details: issuer, rating, coupon, maturity, tranche sizes, IPT, NIC, order book demand.
- Market data feeds: secondary bond prices, yield curves.

### Analysis

- Identify oversubscription levels, attrition, and curve shapes.
- Compare coupon vs. yield vs. spread.
- Highlight NIC impact on pricing.

### Output

- MCP services exposing bond analytics in structured JSON.
- SQL / vector DB storage for structured and unstructured data.
- Context responses ready for dashboards or AI model queries.

## 3. Tech Stack

- Backend framework: FastAPI (Python)
- Protocol layer: MCP server implementation (Model Context Protocol)
- Database:
  - SQL DB (PostgreSQL / MySQL) for structured bond data.
  - Optional vector DB (e.g. Pinecone, Weaviate, pgvector) for unstructured market commentary or research.
- Data models:
  - Bond issuance schema: issuer, rating, coupon, maturity, IPT, NIC, order book stats.
  - Market analytics schema: oversubscription ratio, attrition %, curve shape classification.

## 4. Functional Requirements

### Bond Data Context Service

- MCP service: `bond.data`
- Provides issuer details, tranche info, coupon, and redemption terms.

### Order Book Context Service

- MCP service: `bond.orderbook`
- Provides peak demand, attrition, and oversubscription ratio.

### Curve Shape Context Service

- MCP service: `bond.curve`
- Classifies yield curve as normal, flat, inverted, or humped.

### Pricing Context Service

- MCP service: `bond.pricing`
- Provides IPT, NIC, and final pricing spread.

### Research Query Context Service (Optional)

- MCP service: `bond.research`
- Supports semantic search across Credit Flow Research (CFR) notes and market commentary.

## 5. Non-Functional Requirements

- Performance: handle up to 10,000 bond records with <200 ms query latency.
- Protocol compliance: strict adherence to MCP specifications.
- Security: JWT-based authentication for MCP calls.
- Extensibility: easy integration with dashboards or other MCP clients.

## 6. Deliverables

- MCP server implemented in FastAPI.
- SQL schema for bond data storage.
- Optional vector DB integration for research queries.
- Documentation:
  - MCP service definitions
  - Schema
  - Deployment guide

## 7. Business Glossary

### Bond Market Terms

- Book Runner: Lead bank / underwriter managing the bond issuance, order book, and pricing.
- Syndicate: Group of banks collaborating to distribute and manage a bond issue.
- IPT (Initial Price Talk): Preliminary guidance on expected yield / spread before order book building.
- NIC (New Issue Concession): Extra yield offered compared to existing bonds to attract investors.
- Coupon: Interest rate paid to bondholders, usually semi-annually, based on face value.
- Redemption: Repayment of bond principal at maturity or earlier (callable bonds).
- Order Book: Record of investor demand for a bond issue.
- Peak Order Book: Highest demand level reached during book-building.
- Attrition: Drop in demand between peak and final order book.
- Curve Shape: Yield profile across maturities (normal, flat, inverted, humped).
- Ticker: Short code identifying a security on an exchange.
- Investment Grade: Bonds rated BBB- or higher, considered lower risk.
- CFR (Credit Flow Research): Analysis of credit issuance and investor demand trends.

### Credit Ratings

- AAA: Highest rating, lowest risk.
- AA / A: Strong credit quality, slightly more risk.
- BBB+: Lower investment grade, adequate but more vulnerable to economic changes.
- BB and below: Speculative / junk bonds, higher risk.
- D: Default.

### Technical Terms (PoC Context)

- MCP Server (Model Context Protocol): Backend service exposing structured context for AI models.
- FastAPI: Python framework for building RESTful APIs and MCP services.
- SQL Database: Structured storage for bond data (issuer, coupon, maturity, order book).
- Vector Database: Optional storage for unstructured data (market commentary, CFR notes).
- MCP Services: Protocol-compliant endpoints for retrieving bond analytics (pricing, curve shape, order book).

## 8. PoC Architecture

### High-Level Overview

The architecture ingests bond issuance data, processes analytics such as IPT, NIC, coupon, redemption, order book, and curve shape, and exposes results via MCP services for integration with a mock app or AI model.

### Components

#### Frontend (Mock App)

- Displays bond analytics dashboards.
- Consumes MCP services.
- Could be a simple React / Angular UI or Postman for PoC testing.

#### Backend (MCP Server - FastAPI)

- MCP service layer:
  - Context services for bond data, order book, curve shape, pricing, and research.
- Business logic layer:
  - Modules for calculations: oversubscription, attrition, NIC, and yield curve classification.
- Data access layer:
  - ORM (SQLAlchemy) for SQL DB.
  - Optional vector DB client for semantic search.

#### Database Layer

- SQL DB (PostgreSQL / MySQL): stores structured bond data.
- Vector DB (optional - pgvector / Pinecone / Weaviate): stores unstructured text like CFR notes.

#### Data Sources

- Mock bond issuance data (CSV / JSON).
- Market data feeds (simulated for PoC).

### Data Flow

- Data ingestion: bond issuance data -> SQL DB; research notes -> vector DB.
- Processing: business logic computes oversubscription, attrition, and curve shape; pricing module compares IPT vs. final spread and NIC.
- MCP exposure: MCP services return structured JSON; frontend consumes services for visualization.

## 9. Example MCP Services

- `bond.data` -> Bond details (issuer, coupon, maturity, rating)
- `bond.orderbook` -> Peak demand, attrition, oversubscription ratio
- `bond.curve` -> Yield curve shape classification
- `bond.pricing` -> IPT, NIC, final spread
- `bond.research` -> Semantic search in CFR notes (vector DB)

## 10. Deployment (PoC)

- Local / cloud: Dockerized FastAPI MCP server.
- DB: PostgreSQL container + optional pgvector extension.
- Testing: Mock data injection + MCP service testing via Postman / Swagger UI.
