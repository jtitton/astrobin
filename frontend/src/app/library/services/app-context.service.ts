import { Injectable } from '@angular/core';
import { forkJoin } from "rxjs";
import { flatMap, share } from "rxjs/operators";
import { IUser, IUserProfile } from "./api/user-api.interfaces";
import { UserApiService } from "./api/user-api.service";

export interface IAppContext {
  currentUserProfile: IUserProfile,
  currentUser: IUser
}

@Injectable({
  providedIn: 'root'
})
export class AppContextService {
  private _appContext = {} as IAppContext;

  constructor(public userApi: UserApiService) {
  }

  load(): Promise<any> {
    return forkJoin(
      this.userApi.getCurrentUserProfile().pipe(share()),
      this.userApi.getCurrentUserProfile().pipe(flatMap(userProfile => this.userApi.getUser(userProfile.user)))
    ).toPromise().then((results) => {
      this._appContext = {
        currentUserProfile: results[0],
        currentUser: results[1]
      };
    });
  }

  get(): IAppContext {
    return this._appContext;
  }
}
