workspace {

    model {
        user = person "Analyst" {
            description "User who monitors and investigates bank reconciliations"
        }

        integrationPlatform = softwareSystem "Bank Integration Platform" {
            description "Automates daily reconciliation of positions with multiple custodians, normalizes formats, detects discrepancies, and maintains audit trail."

            webInterface = container "Web Interface" {
                technology "React/Node.js"
                description "Allows the user to view reconciliations, discrepancies, and audit."
            }

            apiGateway = container "API Gateway" {
                technology "Node.js/Express"
                description "Routes requests to internal services."
            }

            custodyAdapterBTG = container "BTG Adapter" {
                technology "Python/SFTP/CSV"
                description "Receives CSV files via SFTP, normalizes to the internal standard."
            }
            custodyAdapterItau = container "Itaú Adapter" {
                technology "Python/REST/Webhook"
                description "Receives real-time data via API/Webhook, normalizes to the internal standard."
            }
            custodyAdapterBradesco = container "Bradesco Adapter" {
                technology "Python/Email/PDF"
                description "Receives emails with PDF, extracts data and normalizes to the internal standard."
            }

            normalizationPipeline = container "Normalization Pipeline" {
                technology "Python"
                description "Validates, extracts, and transforms data from adapters to the common model."
            }

            reconciliationEngine = container "Reconciliation Engine" {
                technology "Python"
                description "Compares custodian positions with the internal system, detects discrepancies, and applies configurable rules."
            }

            alertService = container "Alert Service" {
                technology "Node.js/Email/Slack"
                description "Notifies detected discrepancies according to configuration."
            }

            configService = container "Custodian Configuration" {
                technology "YAML/JSON"
                description "Allows adding new custodians and rules without code."
            }

            auditService = container "Audit Service" {
                technology "Python/PostgreSQL"
                description "Records all process steps for traceability."
            }

            database = container "Database" {
                technology "PostgreSQL"
                description "Stores positions, logs, audit trail, and configurations."
            }

            // Relationships
            user -> webInterface "Views reconciliations, discrepancies, and audit"
            webInterface -> apiGateway "Requests data and reports"
            apiGateway -> normalizationPipeline "Triggers normalization of received data"
            normalizationPipeline -> custodyAdapterBTG "Receives data from BTG Pactual"
            normalizationPipeline -> custodyAdapterItau "Receives data from Itaú BBA"
            normalizationPipeline -> custodyAdapterBradesco "Receives data from Bradesco"
            normalizationPipeline -> reconciliationEngine "Sends normalized data for reconciliation"
            reconciliationEngine -> alertService "Notifies detected discrepancies"
            reconciliationEngine -> auditService "Records reconciliation result"
            reconciliationEngine -> database "Updates reconciled positions"
            configService -> normalizationPipeline "Provides custodian rules and formats"
            configService -> reconciliationEngine "Provides reconciliation and tolerance rules"
            auditService -> database "Persists audit trail"
        }
    }

    views {
        systemContext integrationPlatform {
            include *
            autolayout lr
        }
        container integrationPlatform {
            include *
            autolayout lr
        }
        theme default
    }
}
