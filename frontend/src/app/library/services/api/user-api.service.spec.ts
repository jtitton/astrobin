import { HttpClientTestingModule, HttpTestingController } from "@angular/common/http/testing";
import { TestBed } from '@angular/core/testing';
import { of } from "rxjs";
import { IUser, IUserProfile } from "./user-api.interfaces";

import { UserApiService } from './user-api.service';

describe('UserApiService', () => {
  let service: UserApiService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [UserApiService]
    });

    service = TestBed.get(UserApiService);
    httpMock = TestBed.get(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('getUser should work', () => {
    const mockUser = {
      id: 1,
      username: "foo"
    } as IUser;

    service.getUser(mockUser.id).subscribe(response => {
      expect(response).toEqual(mockUser);
    });

    const req = httpMock.expectOne(`${service.configUrl}/users/${mockUser.id}`);
    expect(req.request.method).toBe("GET");
    req.flush(mockUser);
  });

  it('getCurrentUserProfile should return the authenticated user', () => {
    const mockUserProfile = {
      user: 1
    } as IUserProfile;

    service.getCurrentUserProfile().subscribe(response => {
      expect(response).toEqual(mockUserProfile);
    });

    const req = httpMock.expectOne(`${service.configUrl}/userprofiles/current`);
    expect(req.request.method).toBe("GET");
    req.flush([mockUserProfile]);
  });

  it('getCurrentUserProfile should return null if not authenticated', () => {
    service.getCurrentUserProfile().subscribe(response => {
      expect(response).toEqual(null);
    });

    const req = httpMock.expectOne(`${service.configUrl}/userprofiles/current`);
    expect(req.request.method).toBe("GET");
    req.flush([]);
  });

  it('isAuthenticated should return false if there is no current user profile', () => {
    spyOn(service, 'getCurrentUserProfile').and.returnValue(of(null));
    service.isAuthenticated().subscribe(response => {
      expect(response).toBe(false);
    })
  });

  it('isAuthenticated should return true if there is a current user profile', () => {
    spyOn(service, 'getCurrentUserProfile').and.returnValue(of({user: 1}));
    service.isAuthenticated().subscribe(response => {
      expect(response).toBe(true);
    })
  });
});
