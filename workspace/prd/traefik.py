from phidata.app.traefik import IngressRoute, LoadBalancerProvider
from phidata.infra.k8s.create.core.v1.service import ServiceType

from workspace.settings import (
    use_cache,
    ws_dir_path,
    airflow_enabled,
    superset_enabled,
    traefik_enabled,
)
from workspace.prd.aws_resources import prd_logs_s3_bucket, prd_aws_dp_certificate
from workspace.prd.airflow import prd_airflow_ws, prd_airflow_flower
from workspace.prd.superset import prd_superset_ws
from workspace.prd.settings import (
    prd_key,
    prd_domain,
    services_ng_label,
    topology_spread_key,
    topology_spread_max_skew,
    topology_spread_when_unsatisfiable,
)
from workspace.k8s.whoami import whoami_service, whoami_port

# -*- Kubernetes resources

# Traefik Ingress: For routing web requests within the EKS cluster
routes = [
    {
        "match": f"Host(`whoami.{prd_domain}`)",
        "kind": "Rule",
        "services": [
            {
                "name": whoami_service.service_name,
                "port": whoami_port.service_port,
            }
        ],
    },
]

if airflow_enabled:
    routes.append(
        {
            "match": f"Host(`airflow.{prd_domain}`)",
            "kind": "Rule",
            "services": [
                {
                    "name": prd_airflow_ws.get_ws_service_name(),
                    "port": prd_airflow_ws.get_ws_service_port(),
                }
            ],
        }
    )
    routes.append(
        {
            "match": f"Host(`flower.{prd_domain}`)",
            "kind": "Rule",
            "services": [
                {
                    "name": prd_airflow_flower.get_flower_service_name(),
                    "port": prd_airflow_flower.get_flower_service_port(),
                }
            ],
        }
    )

if superset_enabled:
    routes.append(
        {
            "match": f"Host(`superset.{prd_domain}`)",
            "kind": "Rule",
            "services": [
                {
                    "name": prd_superset_ws.get_app_service_name(),
                    "port": prd_superset_ws.get_app_service_port(),
                }
            ],
        }
    )

traefik_name = "traefik"
traefik_ingress_route = IngressRoute(
    replicas=3,
    name=traefik_name,
    domain_name=prd_domain,
    access_logs=True,
    web_enabled=True,
    web_routes=routes,
    websecure_enabled=True,
    websecure_routes=routes,
    # Use ACM certificate to enable HTTPS
    forward_web_to_websecure=True,
    # Use a LoadBalancer service
    service_type=ServiceType.LOAD_BALANCER,
    # Use a LoadBalancer provided by AWS
    load_balancer_provider=LoadBalancerProvider.AWS,
    # Use a Network Load Balancer: recommended
    use_nlb=True,
    # `ip` or `instance`
    nlb_target_type="ip",
    # `internet-facing` or `internal`
    load_balancer_scheme="internet-facing",
    # You may configure the LoadBalancer using annotations:
    # https://kubernetes-sigs.github.io/aws-load-balancer-controller/v2.2/guide/service/annotations/#annotations
    # service_annotations={
    #     "service.beta.kubernetes.io/aws-load-balancer-name": traefik_name,
    # },
    # Read ACM certificate from a summary file and add the certificate ARN to the service_annotations
    acm_certificate_summary_file=prd_aws_dp_certificate.certificate_summary_file,
    # Write access logs to s3
    access_logs_to_s3=True,
    access_logs_s3_bucket=prd_logs_s3_bucket.name,
    access_logs_s3_bucket_prefix=traefik_name,
    # Enable traefik dashboard at traefik.prd_domain
    dashboard_enabled=True,
    # The dashboard is gated behind a user:password, which is generated using the cmd:
    #   htpasswd -nb user password
    # You can provide the "users:password" list as DASHBOARD_AUTH_USERS in the secrets_file
    secrets_file=ws_dir_path.joinpath("secrets/prd_traefik_secrets.yml"),
    use_cache=use_cache,
    pod_node_selector=services_ng_label,
    topology_spread_key=topology_spread_key,
    topology_spread_max_skew=topology_spread_max_skew,
    topology_spread_when_unsatisfiable=topology_spread_when_unsatisfiable,
    install_crds=False,
)

prd_traefik_apps = [traefik_ingress_route] if traefik_enabled else []
