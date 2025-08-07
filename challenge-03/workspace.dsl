workspace {

    model {
        user = person "Analyst/Trader" {
            description "User who monitors, investigates, and operates assets, FIDCs, and custodians."
        }

        growthPlatform = softwareSystem "Distributed Growth Pricing & Reconciliation Platform" {
            description "Scalable platform for pricing, reconciliation, and management of multiple assets, FIDCs, and custodians."

            webInterface = container "Web Interface" {
                technology "React/Node.js"
                description "Allows the user to view, operate, audit, and configure the system."
            }

            apiGateway = container "API Gateway" {
                technology "Node.js/Express"
                description "Routes requests to internal and external services."
            }

            pricingOrchestrator = container "Pricing Orchestrator" {
                technology "Python/Celery/Kubernetes"
                description "Distributes pricing and reconciliation jobs, manages parallelism, retries, and prioritization."
            }

            reconciliationEngine = container "Reconciliation Engine" {
                technology "Python/Celery/Kubernetes"
                description "Compares positions, detects discrepancies, and applies configurable rules."
            }

            normalizationPipeline = container "Normalization Pipeline" {
                technology "Python"
                description "Validates, extracts, and transforms data from adapters to the common model."
            }

            alertService = container "Alert Service" {
                technology "Node.js/Email/Slack"
                description "Notifies discrepancies according to configuration."
            }

            configService = container "Configuration Service" {
                technology "YAML/JSON/Feature Flags"
                description "Allows adding new assets, FIDCs, custodians, and rules without code."
            }

            auditService = container "Audit Service" {
                technology "Python/PostgreSQL"
                description "Records all steps for traceability and history."
            }

            cache = container "Cache" {
                technology "Redis"
                description "Stores intermediate results and prevents duplication."
            }

            retryQueue = container "Retry Queue" {
                technology "RabbitMQ"
                description "Queues jobs for retry and decouples processing."
            }

            database = container "Database" {
                technology "PostgreSQL/Sharding"
                description "Stores positions, logs, history, configurations, and data partitioning."
            }

            monitoring = container "Monitoring & Tracing" {
                technology "Prometheus/Grafana/OpenTelemetry"
                description "Centralizes metrics, logs, and tracing for troubleshooting and performance."
            }

            // Dynamic adapters for multiple custodians and assets
            adapters = container "Adapters" {
                technology "Python/Node.js/SFTP/REST/Email/Webhook"
                description "Receive data in multiple formats, normalize, and scale via configuration."
            }

            // Main relationships
            user -> webInterface "Operates, monitors, and audits the system"
            webInterface -> apiGateway "Requests pricing, reconciliation, reports, and configurations"
            apiGateway -> pricingOrchestrator "Triggers pricing and reconciliation jobs"
            pricingOrchestrator -> normalizationPipeline "Orchestrates normalization of received data"
            normalizationPipeline -> adapters "Receives data from multiple custodians and assets"
            normalizationPipeline -> reconciliationEngine "Sends normalized data for reconciliation"
            reconciliationEngine -> alertService "Notifies discrepancies"
            reconciliationEngine -> auditService "Records reconciliation results"
            reconciliationEngine -> database "Updates reconciled positions"
            configService -> normalizationPipeline "Provides rules and formats for custodians/assets"
            configService -> reconciliationEngine "Provides reconciliation and tolerance rules"
            auditService -> database "Persists audit trail and history"
            retryQueue -> pricingOrchestrator "Resends failed jobs"
            cache -> pricingOrchestrator "Prevents job duplication"
            // Explicit monitoring relationships
            monitoring -> webInterface "Monitors Web Interface"
            monitoring -> apiGateway "Monitors API Gateway"
            monitoring -> pricingOrchestrator "Monitors Pricing Orchestrator"
            monitoring -> normalizationPipeline "Monitors Normalization Pipeline"
            monitoring -> reconciliationEngine "Monitors Reconciliation Engine"
            monitoring -> alertService "Monitors Alert Service"
            monitoring -> configService "Monitors Configuration Service"
            monitoring -> auditService "Monitors Audit Service"
            monitoring -> cache "Monitors Cache"
            monitoring -> retryQueue "Monitors Retry Queue"
            monitoring -> database "Monitors Database"
            monitoring -> adapters "Monitors Adapters"
        }
    }

    views {
        systemContext growthPlatform {
            include *
            autolayout lr
        }
        container growthPlatform {
            include *
            autolayout lr
        }
        theme default
    }
}
