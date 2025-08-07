workspace {

    model {
        user = person "User" {
            description "Trader or analyst who interacts with the system"
        }

        fidcSystem = softwareSystem "FIDC Pricing System" {
            description "Distributed pricing system for FIDC assets"

            webInterface = container "Web Interface" {
                technology "React/Node.js"
                description "Allows users to trigger pricing, view audit logs and generate reports"
            }

            apiGateway = container "API Gateway" {
                technology "Node.js/Express"
                description "Routes requests to the correct services"
            }

            pricingOrchestrator = container "Pricing Orchestrator" {
                technology "Python/Celery"
                description "Distributes pricing jobs to workers, manages retries and prioritization"
            }

            pricingWorker = container "Pricing Worker" {
                technology "Python"
                description "Executes pricing calculations in parallel, handles complex assets"
            }

            auditService = container "Audit Service" {
                technology "Python"
                description "Stores and retrieves logs of pricing runs, including source, worker, timestamp"
            }

            cache = container "Cache" {
                technology "Redis"
                description "Stores intermediate results, prevents duplicate pricing"
            }

            retryQueue = container "Retry Queue" {
                technology "RabbitMQ"
                description "Queues failed jobs for retry"
            }

            database = container "Database" {
                technology "PostgreSQL"
                description "Stores pricing results and logs"
            }

            anbimaApi = container "ANBIMA API Adapter" {
                technology "Python"
                description "Handles ANBIMA API integration and rate limiting"
            }

            bloombergApi = container "Bloomberg API Adapter" {
                technology "Python"
                description "Handles Bloomberg API integration and failover"
            }

            b3Api = container "B3 API Adapter" {
                technology "Python"
                description "Handles B3 API integration and rate limiting"
            }

            user -> webInterface "Uses system to trigger pricing and access reports"
            webInterface -> apiGateway "Sends pricing trigger or reporting request"
            apiGateway -> pricingOrchestrator "Initiates pricing jobs"
            pricingOrchestrator -> pricingWorker "Distributes pricing jobs"
            pricingWorker -> anbimaApi "Fetches asset prices"
            pricingWorker -> bloombergApi "Fetches asset prices"
            pricingWorker -> b3Api "Fetches asset prices"
            pricingWorker -> cache "Checks for duplicate pricing"
            pricingWorker -> database "Stores pricing results"
            pricingWorker -> auditService "Logs pricing run details"
            pricingWorker -> retryQueue "Queues failed jobs"
            retryQueue -> pricingOrchestrator "Retries failed jobs"
            auditService -> database "Reads/writes audit logs"
        }
    }

    views {
        systemContext fidcSystem {
            include *
            autolayout lr
        }

        container fidcSystem {
            include *
            autolayout lr
        }

        theme default
    }

}
