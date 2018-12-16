import { HttpClient } from "@angular/common/http";
import { Injectable } from '@angular/core';
import { Observable } from "rxjs";
import { map } from "rxjs/operators";
import { BaseApiService } from "./base-api.service";
import { IUser, IUserProfile } from "./user-api.interfaces";

@Injectable({
  providedIn: 'root'
})
export class UserApiService extends BaseApiService {
  configUrl = this.baseUrl + '/common';

  constructor(private http: HttpClient) {
    super();
  }

  getUser(id: number): Observable<IUser> {
    return this.http.get<IUser>(this.configUrl + "/users/" + id);
  }

  getCurrentUserProfile(): Observable<IUserProfile> {
    return this.http.get<IUserProfile[]>(this.configUrl + '/userprofiles/current').pipe(
      map(response => {
        if(response.length > 0) {
          return response[0];
        }

        return null;
      })
    )
  }

  isAuthenticated(): Observable<boolean> {
    return new Observable(observer => {
      this.getCurrentUserProfile().subscribe(userProfile => {
        observer.next(userProfile !== null);
        observer.complete();
      });
    });
  }
}
