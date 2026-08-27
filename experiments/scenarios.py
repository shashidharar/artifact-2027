"""
ARIA Benchmark Scenarios
"""

from models import DeviceState


SCENARIOS = [

    {
        "id": 1,
        "name": "Memory Exhaustion",

        "state": DeviceState(

            cpu_utilization=30,

            memory_utilization=95,

            storage_utilization=40,

            network_latency=20,

            battery_level=90,

            application_running=True,

            security_alert=False,

            health_score=0.70

        )
    },

    {
        "id": 2,
        "name": "Storage Exhaustion",

        "state": DeviceState(

            cpu_utilization=35,

            memory_utilization=40,

            storage_utilization=96,

            network_latency=20,

            battery_level=88,

            application_running=True,

            security_alert=False,

            health_score=0.70

        )
    },

    {
        "id": 3,
        "name": "Application Crash",

        "state": DeviceState(

            cpu_utilization=20,

            memory_utilization=40,

            storage_utilization=40,

            network_latency=15,

            battery_level=90,

            application_running=False,

            security_alert=False,

            health_score=0.60

        )
    },

    {
        "id": 4,
        "name": "Network Latency",

        "state": DeviceState(

            cpu_utilization=20,

            memory_utilization=40,

            storage_utilization=40,

            network_latency=350,

            battery_level=90,

            application_running=True,

            security_alert=False,

            health_score=0.65

        )
    },

    {
        "id": 5,
        "name": "Security Threat",

        "state": DeviceState(

            cpu_utilization=30,

            memory_utilization=45,

            storage_utilization=40,

            network_latency=20,

            battery_level=85,

            application_running=True,

            security_alert=True,

            health_score=0.55

        )
    }

]