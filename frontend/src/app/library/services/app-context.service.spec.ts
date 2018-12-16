import { fakeAsync, TestBed, tick } from '@angular/core/testing';
import { of } from "rxjs";
import { UserApiService } from "./api/user-api.service";

import { AppContextService } from './app-context.service';

class MockUserApiService {
  getUser = jasmine.createSpy('getUser').and.returnValue(of({id: 1}));
  getCurrentUserProfile = jasmine.createSpy('getCurrentUserProfile').and.returnValue(of({user: 1}));
}

describe('AppContextService', () => {
  let service: AppContextService;

  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [
        {provide: UserApiService, useClass: MockUserApiService}
      ]
    });
    service = TestBed.get(AppContextService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('currentUserProfile should be available',() => {
    service.load().then((response) => {
      expect(response.get().currentUserProfile.user).toEqual(1);
    });
  });

  it('currentUser should be available',() => {
    service.load().then((response) => {
      expect(response.get().currentUser.id).toEqual(1);
    });
  });
});
