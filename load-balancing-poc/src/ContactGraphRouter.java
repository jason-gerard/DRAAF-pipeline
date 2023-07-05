import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

public interface ContactGraphRouter {
    public HashMap<Id, RouteTable> computeAllRoutes(List<Id> ids, List<Contact> contactPlan);
}
