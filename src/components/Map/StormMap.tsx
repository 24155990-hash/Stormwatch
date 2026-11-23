import { APIProvider, Map } from '@vis.gl/react-google-maps';
const API_KEY = import.meta.env.VITE_GOOGLE_MAPS_API_KEY as string | undefined;
const INDIA_CENTER = {lat :15, lng:78};
export default function StormMap(){
    if (!API_KEY){
        return <p>Missing VITE_GOOGLE_MAPS_API_KEY, Check your .env.local file. </p>;
    }
    return (
    <APIProvider apiKey={API_KEY}>
      <Map
        defaultCenter={INDIA_CENTER}
        defaultZoom={6}
        mapId="DEMO_MAP_ID"
        gestureHandling="greedy"
        style={{ width: '100%', height: '100%' }}
      />
    </APIProvider>
  );
}
