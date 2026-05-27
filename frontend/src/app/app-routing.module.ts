import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { DashboardComponent } from './dashboard/dashboard.component';
import { SignupComponent } from './login/signup.component';
import { LoginComponent } from './login/login.component';
import { UserComponent } from './user/user.component';
import { RoleComponent } from './role/role.component';
import { CollegeComponent } from './college/college.component';
import { CourseComponent } from './course/course.component';
import { SubjectComponent } from './subject/subject.component';
import { MarksheetComponent } from './marksheet/marksheet.component';
import { TimetableComponent } from './timetable/timetable.component';
import { FacultyComponent } from './faculty/faculty.component';
import { StudentComponent } from './student/student.component';
import { UserListComponent } from './user/user-list.component';
import { RoleListComponent } from './role/role-list.component';
import { CollegeListComponent } from './college/college-list.component';
import { CourseListComponent } from './course/course-list.component';
import { SubjectListComponent } from './subject/subject-list.component';
import { FacultyListComponent } from './faculty/faculty-list.component';
import { MarksheetListComponent } from './marksheet/marksheet-list.component';
import { StudentListComponent } from './student/student-list.component';
import { TimetableListComponent } from './timetable/timetable-list.component';
import { ChangepasswordComponent } from './user/changepassword.component';
import { ForgetpasswordComponent } from './login/forgetpassword.component';
import { EnergyComponent } from './energy/energy.component';
import { EnergyListComponent } from './energy/energy-list.component';
import { TopicComponent } from './topic/topic.component';
import { TopicListComponent } from './topic/topic-list.component';
import { LightComponent } from './light/light.component';
import { LightListComponent } from './light/light-list.component';
import { PodcastComponent } from './podcast/podcast.component';
import { PodcastListComponent } from './podcast/podcast-list.component';
import { CourierComponent } from './courier/courier.component';
import { CourierListComponent } from './courier/courier-list.component';
import { HotelComponent } from './hotel/hotel.component';
import { HotelListComponent } from './hotel/hotel-list.component';
import { CloudComponent } from './cloud/cloud.component';
import { CloudListComponent } from './cloud/cloud-list.component';





const routes: Routes = [
  {
    path: '',
    pathMatch: 'full',
    redirectTo: 'dashboard'
  },
  {
    path: 'dashboard',
    component: DashboardComponent
  },
  {
    path: 'login',
    component: LoginComponent
  },
  {
    path: 'signup',
    component: SignupComponent
  },
  {
    path: 'user',
    component: UserComponent
  },
  {
    path: 'role',
    component: RoleComponent
  },
  {
    path: 'college',
    component: CollegeComponent
  },
  {
    path: 'course',
    component: CourseComponent
  },
  {
    path: 'subject',
    component: SubjectComponent
  },
  {
    path: 'marksheet',
    component: MarksheetComponent
  },
  {
    path: 'timetable',
    component: TimetableComponent
  },
  {
    path: 'faculty',
    component: FacultyComponent
  },
  {
    path: 'student',
    component: StudentComponent
  },
  {
    path: 'energy',
    component: EnergyComponent
  },
  {
    path: 'topic',
    component: TopicComponent
  },
  {
    path: 'light',
    component: LightComponent
  },
  {
    path: 'podcast',
    component: PodcastComponent
  },
  {
    path: 'courier',
    component: CourierComponent
  },
  {
    path: 'hotel',
    component: HotelComponent
  },
  {
    path: 'cloud',
    component: CloudComponent
  },

  {
    path: 'userlist',
    component: UserListComponent
  },
  {
    path: 'user/:id',
    component: UserComponent
  },
  {
    path: 'rolelist',
    component: RoleListComponent
  },
  {
    path: 'role/:id',
    component: RoleComponent
  },
  {
    path: 'collegelist',
    component: CollegeListComponent
  },
  {
    path: 'college/:id',
    component: CollegeComponent
  },
  {
    path: 'courselist',
    component: CourseListComponent
  },
  {
    path: 'course/:id',
    component: CourseComponent
  },
  {
    path: 'subjectlist',
    component: SubjectListComponent
  },
  {
    path: 'subject/:id',
    component: SubjectComponent
  },
  {
    path: 'facultylist',
    component: FacultyListComponent
  },
  {
    path: 'faculty/:id',
    component: FacultyComponent
  },
  {
    path: 'marksheetlist',
    component: MarksheetListComponent
  },
  {
    path: 'marksheet/:id',
    component: MarksheetComponent
  },
  {
    path: 'studentlist',
    component: StudentListComponent
  },
  {
    path: 'student/:id',
    component: StudentComponent
  },
  {
    path: 'timetablelist',
    component: TimetableListComponent
  },
  {
    path: 'timetable/:id',
    component: TimetableComponent
  },
  {
    path: 'energylist',
    component: EnergyListComponent
  },
  {
    path: 'energy/:id',
    component: EnergyComponent
  },
  {
    path: 'topiclist',
    component: TopicListComponent
  },
  {
    path: 'topic/:id',
    component: TopicComponent
  },
  {
    path: 'lightlist',
    component: LightListComponent
  },
  {
    path: 'light/:id',
    component: LightComponent
  },
  {
    path: 'podcastlist',
    component: PodcastListComponent
  },
  {
    path: 'podcast/:id',
    component: PodcastComponent
  },
  {
    path: 'courierlist',
    component: CourierListComponent
  },
  {
    path: 'courier/:id',
    component: CourierComponent
  },
  {
    path: 'hotellist',
    component: HotelListComponent
  },
  {
    path: 'hotel/:id',
    component: HotelComponent
  },
  {
    path: 'cloudlist',
    component: CloudListComponent
  },
  {
    path: 'cloud/:id',
    component: CloudComponent
  },
  {
    path: 'changepassword',
    component: ChangepasswordComponent
  },
  {
    path: 'forgetpassword',
    component: ForgetpasswordComponent
  }

];

@NgModule({

  // imports: [RouterModule.forRoot(routes)],

  imports: [RouterModule.forRoot(routes, { useHash: true })],
  exports: [RouterModule]
})
export class AppRoutingModule { }