// describes a format for how our data is represented 

export type TrackType =
  | 'main'
  | 'PROVISIONAL'
  | 'US-PROVISIONAL'
  | 'spur-merge';

//this is one single entry of a cyclone
export interface CycloneSummary {
  id: string;
  name: string;
  season: number;
  startTime: string;
  endTime: string;
  startLat: number;
  startLon: number;
  maxWindKt: number | null;
  minPressureMb: number | null;
  trackType: TrackType;
}

//one single estimated entry in the track file of a storm, so basically a single point 
export interface TrackPoint {
  time: string;
  lat: number;
  lon: number;
  windKt: number | null;
  pressureMb: number | null;
  recorded: boolean;
}