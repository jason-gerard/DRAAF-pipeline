import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.stream.Collectors;

public class SDNController {
    public ContactGraphRouter router;
    public List<Satellite> satellites;
    public List<Contact> contactPlan;

    public List<Contact> mutateContactPlan(List<Contact> contactPlan) { return contactPlan; }
    
    public HashMap<Id, RouteTable> computeLoadBalancedRoutes() {
        List<Contact> weightedContactPlan = this.mutateContactPlan(this.contactPlan);
        
        List<Id> ids = satellites.stream().map(satellite -> satellite.id).toList();
        return this.router.computeAllRoutes(ids, weightedContactPlan);
    }

    public void distributeRoutes(HashMap<Id, RouteTable> routeTablesBySource) {}
    
    public void updateStatus(Satellite satellite) {}
}
