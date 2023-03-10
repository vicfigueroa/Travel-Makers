import { useEffect, useState } from "react";
import { useNavigate } from 'react-router-dom';
import BulmaInput from './BulmaInput';
import trip from './vids/trip.mp4';
import { useAddTripMutation } from './store/tripsApi';
import ErrorNotification from "./ErrorNotification";



function TripForm() {
    const navigate = useNavigate();
    const [name, setName] = useState('');
    const [destination, setDestination] = useState('');
    const [start, setStart] = useState('');
    const [end, setEnd] = useState('');
    const [people, setPeople] = useState('');
    const [error, setError] = useState('');
    const [createTrip, result] = useAddTripMutation();

    async function handleSubmit(e) {
        e.preventDefault();
        createTrip({trip_name: name, destination, start_date: start, end_date: end, num_people: people});
    }
    useEffect(() => {
      if (result.isSuccess) {
          navigate("/trips");
      } else if (result.isError) {
          setError(result.error);
      }
    }, [result, navigate, error])

    return (

      <><div className='sign-vid'>
        <video src={trip} autoPlay loop muted />
      </div><div className="container" style={{
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        position: "absolute",
        top: "40%",
        left: "50%",
        transform: "translate(-40%, -40%)",
        boxShadow: '1px 2px 5px black',
        backgroundColor: "#f2f2f2",
        borderRadius: 4,
        border: "1.75px solid black",
        width: '230px',
        height: "375px",
      }}>

          <div className="columns is-centered">
            <div className="column is-one-third">
              <ErrorNotification error={error} />
              <form onSubmit={handleSubmit}>
                <BulmaInput
                  label="Trip name"
                  id="name"
                  placeholder="Summer Trip"
                  value={name}
                  onChange={setName} />
                <BulmaInput
                  label="Destination"
                  id="destination"
                  placeholder="Hawaii"
                  value={destination}
                  onChange={setDestination} />
                <BulmaInput
                  label="Start Date"
                  id="start"
                  type="date"
                  placeholder="YYYY-MM-DD"
                  value={start}
                  onChange={setStart} />
                <BulmaInput
                  label="End Date"
                  id="end"
                  type="date"
                  placeholder="YYYY-MM-DD"
                  value={end}
                  onChange={setEnd} />
                <BulmaInput
                  label="Number of people"
                  id="people"
                  placeholder="2"
                  value={people}
                  onChange={setPeople} />
                <div className="field">
                  <button className="btn btn-dark btn-sm">Save</button>
                </div>
              </form>
            </div>
          </div>
        </div></>
    )
}

export default TripForm;
