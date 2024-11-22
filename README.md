# Architecture and Solution Overview
---
<img width="1283" alt="image (2) (1)" src="https://github.com/user-attachments/assets/2bc8775e-de5a-4662-af27-6d5c094fe4c5">

## Key Features of the Solution

### Streamlit in ECS
- Deployed in ECS for faster, containerized deployments compared to EC2.
- Easily adaptable to other compute environments.

### Containerization Benefits
- Provides isolated environments, ensuring consistent deployments across different setups.

### Tooling Selection
- **Front-End Framework**: Streamlit chosen for ease of building data applications for data analysts and data engineers.
- **Python Implementation**: Python framework used to build the front end (Streamlit).
- **Time-Saving Components**: Built-in Streamlit components reduced the need for custom UI coding.

### Infrastructure Setup
- **AWS as the Cloud Provider**: Chosen for organizational support, team experience, and sandbox availability.
- **Public Subnets**: Default VPC and subnet configurations for quick setup, though future segregation is planned.
- **Cost Considerations**: Focused on maintaining a consistent environment while minimizing costs.

### Database Choice
- **Postgres**: Selected for its vectorization capabilities and full-text search support, critical for generating accurate SQL query results.
- Initial configuration placed the database in a public subnet for simplicity.

### Model Selection
- **Amazon Bedrock Model (Claude Sonnet 3.5)**: Chosen for fast response times and strong code generation capabilities, essential for generating SQL queries.

### Code Logic and Query Execution
- **LangChain Usage**: Two chains interact with Bedrock:
  1. Convert user queries into SQL queries.
  2. Convert SQL results into natural language responses.
- **Prompt Engineering**: Ensures SQL queries or natural language responses adhere to rules for accurate output.
- **Query Execution**: Queries executed against Postgres, with results fed back for natural language conversion.

![chat-with-mysql-chain-langchain](https://github.com/user-attachments/assets/37a776b7-1d60-47c2-b729-ca2322e65112)
---

## Future Improvements

### Planned Enhancements
1. **Memory Store**: Make memory non-local (Database Persistence) to retain query history across sessions.
2. **Avoid Hard-Coded Configurations**: Ensure easier updates and maintainability (Prompting rules).
3. **Security Improvements**: Privatize (Private Subnets) the database and adopt best practices.

---
