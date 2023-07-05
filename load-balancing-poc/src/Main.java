import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

public class Main {
    public static void main(String[] args) {
        // Initialization
        SDNController controller = new SDNController();
        
        List<Satellite> satellites = new ArrayList<>();
        for (int i = 0; i < 10; i++) {
            Satellite satellite = new Satellite();
            satellites.add(satellite);
            controller.satellites.add(satellite);
        }

        // Start of scenario
        
        // Contact plan is received / computed
        List<Contact> contactPlan = new ArrayList<>();
        controller.contactPlan = contactPlan;

        // Satellites push their network status to SDN controller
        for (Satellite satellite : satellites) {
            controller.updateStatus(satellite);
        }
        
        // At pre-defined time a route from every node to every other node is computed using the load balancing
        // algorithm and routing algorithm
        HashMap<Id, RouteTable> routeTablesBySource = controller.computeLoadBalancedRoutes();
        
        // Routing tables are distributed to each satellite
        controller.distributeRoutes(routeTablesBySource);
    }
}
