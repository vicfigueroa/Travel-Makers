from pydantic import BaseModel
from typing import Optional, List
from queries.pool import pool
from datetime import date
from queries.accounts import AccountOut



class Error(BaseModel):
    message: str


class TripIn(BaseModel):
    trip_name: str
    destination: str
    start_date: date
    end_date: date
    num_people: int


class TripOut(BaseModel):
    id: int
    trip_name: str
    destination: str
    start_date: date
    end_date: date
    num_people: int

class TripRepository:
    def create_trip(self, trip: TripIn, user_id: int) -> TripOut:
        try:
            with pool.connection() as conn:
                with conn.cursor() as db:
                    result = db.execute(
                        """
                        insert into trips
                            (trip_name, destination, start_date, end_date, num_people, user_id)
                        values
                            (%s, %s, %s, %s, %s, %s)
                        returning id;
                        """,
                        [
                            trip.trip_name,
                            trip.destination,
                            trip.start_date,
                            trip.end_date,
                            trip.num_people,
                            user_id,
                        ]
                    )
                    id=result.fetchone()[0]
                    return self.trip_in_to_out(id, trip)
        except Exception as e:
            print(e)
            return {"message": "create did not work"}

    def get_trip(self, trip_id: int):
        try:
            with pool.connection() as conn:
                with conn.cursor() as db:
                    result =db.execute(
                        """
                        select id
                        , trip_name
                        , destination
                        , start_date
                        , end_date
                        , num_people
                        from trips
                        where id = %s
                        """,
                        [trip_id]
                    )
                    record = result.fetchone()
                    print(record)
                    if record is None:
                        return None
                    return self.record_to_trip_out(record)
        except Exception as e:
            print(e)
            return {"message": "could not get that trip"}

    def trip_in_to_out(self, id:int, trip:TripIn):
        old_data=trip.dict()
        return TripOut(id=id, **old_data)

    def record_to_trip_out(self, record):
        return TripOut(
            id=record[0],
            trip_name=record[1],
            destination=record[2],
            start_date=record[3],
            end_date=record[4],
            num_people=record[5]
        )

    # def trip_record_to_dict(self, record, description):
    #     trip = None
    #     if record is not None:
    #         trip = {}
    #         trip_fields = [
    #             "trip_id",
    #             "trip_name",
    #             "destination",
    #             "start_date",
    #             "end_date",
    #             "num_people",
    #         ]
    #         for i, column in enumerate(description):
    #             if column.name in trip_fields:
    #                 trip[column.name] = record[i]
    #         trip["id"] = trip["trip_id"]
            # account = {}
            # account_fields = [
            #     "user_id",
            # ]
            # for i, column in enumerate(description):
            #     if column.name in account_fields:
            #         account[column.name] = record[i]
            # account["id"] = account["user_id"]

            # flight = {}
            # flight_fields = [
            #     "flight_id",
            #     "number",
            # ]
            # for i, column in enumerate(description):
            #     if column.name in flight_fields:
            #         flight[column.name] = record[i]
            # flight["id"] = flight["flight_id"]

            # hotel = {}
            # hotel_fields = [
            #     "hotel_id",
            #     "hotel_name",
            # ]
            # for i, column in enumerate(description):
            #     if column.name in hotel_fields:
            #         hotel[column.name] = record[i]
            # hotel["id"] = hotel["hotel_id"]

            # activity = {}
            # activity_fields = [
            #     "activity_id",
            #     "activity_name",
            # ]
            # for i, column in enumerate(description):
            #     if column.name in activity_fields:
            #         activity[column.name] = record[i]
            # activity["id"] = activity["activity_id"]
        return trip
