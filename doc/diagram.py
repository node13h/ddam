from diagrams import Cluster, Diagram, Edge
from diagrams.custom import Custom
from diagrams.elastic.elasticsearch import Beats, Elasticsearch
from diagrams.onprem.monitoring import Prometheus

with Diagram(
    "Architecture", show=False, direction="LR", graph_attr={"splines": "true"}
):
    upstream1 = Custom("Upstream router", "router.png")
    upstream2 = Custom("Upstream router", "router.png")
    downstream = Custom("Downstream router", "router.png")
    lan1 = Custom("LAN", "cloud.png")
    lan2 = Custom("LAN", "cloud.png")
    filebeat = Beats("Filebeat")
    es = Elasticsearch("Elasticsearch")
    ddam = Custom("DDAM", "ddam.png")

    with Cluster("Edge router"):
        us_int1 = Custom("L3 interface", "dot.png")
        us_int2 = Custom("L3 interface", "dot.png")
        ds_int = Custom("L3 interface", "dot.png")
        lan_int1 = Custom("L3 interface", "dot.png")
        lan_int2 = Custom("L3 interface", "dot.png")

        router = Custom("", "router.png")

        [us_int1, us_int2, ds_int, lan_int1, lan_int2] - Edge(color="gray") - router

        netflow = Custom("NetFlow exporter", "flow.png")

        (
            us_int1
            - Edge(xlabel="ingress", style="dashed", tailport="e", headport="n")
            - netflow
        )
        (
            us_int2
            - Edge(xlabel="ingress", style="dashed", tailport="e", headport="s")
            - netflow
        )

    upstream1 - us_int1
    upstream2 - us_int2
    downstream - ds_int
    lan1 - lan_int1
    lan2 - lan_int2

    netflow >> Edge(label="NetFlow (UDP)") >> filebeat
    filebeat >> es

    es << Edge(label="poll") << ddam

    (
        ddam
        >> Edge(
            constraint="false",
            color="red",
            xlabel="BGP BH route announce",
            fontcolor="red",
        )
        >> upstream1
    )
    (
        ddam
        >> Edge(
            constraint="false",
            color="red",
            xlabel="BGP BH route announce",
            fontcolor="red",
        )
        >> upstream2
    )

    ddam << Prometheus("Prometheus")
    ddam >> Custom("SMTP", "smtp.png")
