import datetime
from enum import Enum
from uuid import uuid4

from src.application_tracker.constants.application_constants import APPLICATIONS_PATH
from src.application_tracker.utils.io_utils import read_pkl_file, dump_pkl_file


class ApplicationStatus(Enum):
    APPLIED = "Applied"
    CONTACTED = "Contacted"
    INTERVIEW_SCHEDULED = "Interview Scheduled"
    WAITING = "Waiting for Response (Post Interview)"
    REJECTED = "Rejected"
    OFFER = "Offer Extended"
    NEGOTIATING = "Offer Under Negotiation"
    ACCEPTED = "Offer Accepted"


class Application:
    def __init__(self):
        self._internal_app_id: str | None = None
        self._internal_app_id = self.internal_app_id
        self._application_id: str | None = None
        self._company: str | None = None
        self._hiring_manager: str | None = None
        self._poc: str | None = None
        self._job_description_link: str | None = None
        self._application_portal_link: str | None = None
        self._application_date: datetime.datetime | None = None
        self._follow_up_date: datetime.datetime | None = None
        self._status: ApplicationStatus | None = None
        self._interviewed: bool | None = None
        self._no_interviews: int | None = None
        self._salary_range: str | None = None
        self._proposed_salary: int | None = None

    def as_dict(self):
        output = {
            "internal_application_id": self.internal_app_id,
            "application_id": self.application_id,
            "company": self.company,
            "hiring_manager": self.hiring_manager,
            "poc": self.poc,
            "job_description_link": self.job_description_link,
            "application_portal_link": self.application_portal_link,
            "application_date": self.application_date,
            "follow_up_date": self.follow_up_date,
            "status": self.status,
            "interviewed": self.interviewed,
            "no_interviews": self.no_interviews,
            "salary_range": self.salary_range,
            "proposed_salary": self.proposed_salary,
        }
        return output

    @property
    def internal_app_id(self):
        if self._internal_app_id is None:
            self._internal_app_id = str(uuid4())
        return self._internal_app_id

    @internal_app_id.setter
    def internal_app_id(self, internal_app_id: None | str):
        self._internal_app_id = internal_app_id

    @property
    def application_id(self):
        return self._application_id

    @application_id.setter
    def application_id(self, application_id: str):
        self._application_id = application_id

    @property
    def company(self):
        return self._company

    @company.setter
    def company(self, company: str):
        self._company = company

    @property
    def hiring_manager(self):
        return self._hiring_manager

    @hiring_manager.setter
    def hiring_manager(self, hiring_manager: str):
        self._hiring_manager = hiring_manager

    @property
    def poc(self):
        return self._poc

    @poc.setter
    def poc(self, poc: str):
        self._poc = poc

    @property
    def job_description_link(self):
        return self._job_description_link

    @job_description_link.setter
    def job_description_link(self, job_description_link: str):
        self._job_description_link = job_description_link

    @property
    def application_portal_link(self):
        return self._application_portal_link

    @application_portal_link.setter
    def application_portal_link(self, application_portal_link: str):
        self._application_portal_link = application_portal_link

    @property
    def application_date(self):
        return self._application_date

    @application_date.setter
    def application_date(self, application_date: datetime.datetime):
        self._application_date = application_date

    @property
    def follow_up_date(self):
        return self._follow_up_date

    @follow_up_date.setter
    def follow_up_date(self, follow_up_date: datetime.datetime):
        self._follow_up_date = follow_up_date

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status: ApplicationStatus):
        self._status = status

    @property
    def interviewed(self):
        return self._interviewed

    @interviewed.setter
    def interviewed(self, interviewed: bool):
        self._interviewed = interviewed

    @property
    def no_interviews(self):
        return self._no_interviews

    @no_interviews.setter
    def no_interviews(self, no_interviews: int):
        self._no_interviews = no_interviews

    @property
    def salary_range(self):
        return self._salary_range

    @salary_range.setter
    def salary_range(self, salary_range: str):
        self._salary_range = salary_range

    @property
    def proposed_salary(self):
        return self._proposed_salary

    @proposed_salary.setter
    def proposed_salary(self, proposed_salary: int):
        self._proposed_salary = proposed_salary

    def save_application(self):
        applications = self.load_applications()
        if applications is None:
            applications = {}
        applications[self.internal_app_id] = self
        dump_pkl_file(path=APPLICATIONS_PATH, data=applications)

    @staticmethod
    def load_applications():
        applications = read_pkl_file(path=APPLICATIONS_PATH)
        if applications is None:
            temp_app = Application()
            applications = {temp_app.internal_app_id: temp_app}
        return applications

    @staticmethod
    def save_applications(applications: dict):
        if applications is None:
            return
        dump_pkl_file(path=APPLICATIONS_PATH, data=applications)
