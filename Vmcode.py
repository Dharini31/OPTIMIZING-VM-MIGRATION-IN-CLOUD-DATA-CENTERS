import numpy as np

# Define Hosts with their properties (for demonstration)
hosts = {
    0: {'cpu_capacity': 100, 'memory_capacity': 256, 'cpu_usage': 85, 'memory_usage': 200, 'energy_efficiency': 0.8, 'leaf_switch': 0, 'vms': [0, 1]},  # Host 0 is over-utilized
    1: {'cpu_capacity': 100, 'memory_capacity': 256, 'cpu_usage': 50, 'memory_usage': 140, 'energy_efficiency': 0.7, 'leaf_switch': 1, 'vms': []},  # Host 1 has capacity
    2: {'cpu_capacity': 100, 'memory_capacity': 256, 'cpu_usage': 30, 'memory_usage': 100, 'energy_efficiency': 0.85, 'leaf_switch': 0, 'vms': []},  # Host 2 has capacity
    3: {'cpu_capacity': 100, 'memory_capacity': 256, 'cpu_usage': 60, 'memory_usage': 150, 'energy_efficiency': 0.75, 'leaf_switch': 2, 'vms': []},
    4: {'cpu_capacity': 100, 'memory_capacity': 256, 'cpu_usage': 70, 'memory_usage': 180, 'energy_efficiency': 0.65, 'leaf_switch': 1, 'vms': []},
}


# Define Virtual Machines (VMs)
vms = {
    0: {'cpu_usage': 20, 'memory_usage': 64},  # VM 0 can be migrated
    1: {'cpu_usage': 30, 'memory_usage': 80},  # VM 1 can also be migrated
    2: {'cpu_usage': 30, 'memory_usage': 96},  # VM 2 is also a candidate
}


# Function to calculate the host's utilization history
def get_host_utilization_history(host, T):
    real_data = [0.6, 0.7, 0.85, 0.9, 0.75, 0.65, 0.8, 0.9, 0.7, 0.5]  # Example historical data
    return real_data[:T]

# Function to calculate energy consumption for the host
def calculate_energy_efficiency(host, vm):
    return host['energy_efficiency'] * (host['cpu_usage'] + vm['cpu_usage']) / host['cpu_capacity']

# Function to check if adding a VM violates the SLAV (capacity violation)
def check_sla_violation(host, vm):
    return (host['cpu_usage'] + vm['cpu_usage'] <= host['cpu_capacity'] and
            host['memory_usage'] + vm['memory_usage'] <= host['memory_capacity'])

# Function to calculate correlation coefficient between VM and Host load
def get_correlation_coefficient(vm, host):
    # Adjust correlation for testing purposes
    return 0.5  # Set a constant correlation for simplification

# Function to detect over-utilized hosts
def get_overutilized_hosts():
    overutilized_hosts = []
    for host_id, host in hosts.items():
        utilization_history = get_host_utilization_history(host, T=10)
        count = 0
        thrhigh = update_utilization_threshold(get_EC_level())
        for utilization in utilization_history:
            if utilization > thrhigh:
                count += 1
            if count > 3:
                overutilized_hosts.append(host_id)
    return overutilized_hosts

# Function to update utilization threshold based on energy consumption level (EC)
def update_utilization_threshold(ec_level):
    return 0.7 * ec_level

# Function to get current energy consumption level
def get_EC_level():
    return np.random.uniform(0.1, 1.0)

# Function to select the best host based on energy efficiency, SLAV, and topology
def select_destination_host(source_host, vm):
    best_host = None
    best_score = float('inf')

    for host_id, host in hosts.items():
        if host_id == source_host:
            continue

        if check_sla_violation(host, vm):
            energy_efficiency_score = calculate_energy_efficiency(host, vm)
            topology_score = topology_aware_selection(source_host, host_id)
            total_score = energy_efficiency_score * 0.7 + topology_score * 0.3

            if total_score < best_score:
                best_score = total_score
                best_host = host_id

    return best_host

# Function to check topology distance (Leaf-Spine Topology Awareness)
def topology_aware_selection(source_host, destination_host):
    if hosts[source_host]['leaf_switch'] == hosts[destination_host]['leaf_switch']:
        return 1
    else:
        return 2

# Function to migrate VM
def migrate_vm(source_host, vm_id):
    vm = vms[vm_id]
    destination_host = select_destination_host(source_host, vm)

    if destination_host is not None:
        hosts[destination_host]['vms'].append(vm_id)
        hosts[source_host]['vms'].remove(vm_id) if vm_id in hosts[source_host]['vms'] else None
        print(f"VM {vm_id} migrated from Host {source_host} to Host {destination_host}.")
    else:
        print(f"No suitable host found for migrating VM {vm_id} from Host {source_host}.")

# Main simulation
def run_simulation():
    overutilized_hosts = get_overutilized_hosts()

    if not overutilized_hosts:
        print("No overutilized hosts found.")

    for source_host in overutilized_hosts:
        print(f"Source Host {source_host} has {len(hosts[source_host]['vms'])} VMs before migration.")
        migratable_vms = [vm_id for vm_id in hosts[source_host]['vms'] if get_correlation_coefficient(vms[vm_id], hosts[source_host]) > 0.1]

        if migratable_vms:
            for vm_id in migratable_vms:
                correlation = get_correlation_coefficient(vms[vm_id], hosts[source_host])
                print(f"VM {vm_id} correlation with Host {source_host}: {correlation}")

            vm_id = migratable_vms[0]  # Example: Pick the first VM
            migrate_vm(source_host, vm_id)
            print(f"Source Host {source_host} has {len(hosts[source_host]['vms'])} VMs after migration.")
        else:
            print(f"No VMs with strong correlation for migration from Host {source_host}.")

# Run the migration simulation
run_simulation()