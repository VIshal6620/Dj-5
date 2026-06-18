import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class EndpointServiceService {

  constructor() { }

  public SERVER_URL = "http://localhost:8000/orsapi";
  public USER = this.SERVER_URL + "/User";
  public ROLE = this.SERVER_URL + "/Role";
  public COLLEGE = this.SERVER_URL + "/College";
  public MARKSHEET = this.SERVER_URL + "/Marksheet";
  public STUDENT = this.SERVER_URL + "/Student";
  public SUBJECT = this.SERVER_URL + "/Subject";
  public COURSE = this.SERVER_URL + "/Course";
  public TIMETABLE = this.SERVER_URL + "/TimeTable";
  public FACULTY = this.SERVER_URL + "/Faculty";
  public ENERGY = this.SERVER_URL + "/Energy";
  public TOPIC = this.SERVER_URL + "/Topic";
  public LIGHT = this.SERVER_URL + "/Light";
  public PODCAST = this.SERVER_URL + "/Podcast"
  public COURIER = this.SERVER_URL + "/Courier"
  public HOTEL = this.SERVER_URL + "/Hotel"
  public CLOUD = this.SERVER_URL + "/Cloud"
  public CAR = this.SERVER_URL + "/Car"
  public CLAIM = this.SERVER_URL + "/Claim"
  public REPOSITORY = this.SERVER_URL + "/Repository"
  public COMPLAINT = this.SERVER_URL + "/Complaint"
  public JOB = this.SERVER_URL + "/Job"
}