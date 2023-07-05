import java.util.HashMap;

public class Satellite {
    public Id id;
    public SatelliteStatus status;
    public HashMap<Satellite, LinkStatus> linkStatuses;
    
    public RouteTable routeTable;
}
