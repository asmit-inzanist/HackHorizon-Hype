import "./NearbyClinics.css";

const clinics = [
  {
    id: 1,
    name: "City Veterinary Hospital",
    address: "123 Vet Street, New York",
    time: "24/7 Emergency",
    distance: "1.2 km away",
    alwaysOpen: true
  },
  {
    id: 2,
    name: "PetCare Clinic",
    address: "456 Animal Ave, New York",
    time: "8 AM - 10 PM",
    distance: "2.5 km away"
  },
  {
    id: 3,
    name: "Animal Wellness Center",
    address: "789 Care Lane, New York",
    time: "9 AM - 9 PM",
    distance: "3.8 km away"
  },
  {
    id: 4,
    name: "Emergency Pet Care",
    address: "321 Rescue Blvd, New York",
    time: "24/7 Emergency",
    distance: "4.2 km away",
    alwaysOpen: true
  }
];

export default function NearbyClinics() {
  return (
    <div className="clinicsPage">

      <div className="clinicsHeader">
        <div>
          <h2>Nearby Clinics</h2>
          <span>4 clinics found</span>
        </div>

        <div className="viewToggle">
          <button className="active">☰ List</button>
          <button>🗺 Map</button>
        </div>
      </div>

      <div className="clinicGrid">
        {clinics.map(c => (
          <div className="clinicCard" key={c.id}>

            <div className="clinicInfo">
              <div className="clinicTitle">
                {c.name}
                {c.alwaysOpen && <span className="badge">24/7</span>}
              </div>

              <div className="row">📍 {c.address}</div>
              <div className="row">⏰ {c.time}</div>
              <div className="distance">➤ {c.distance}</div>
            </div>

            <div className="clinicActions">
              <button>📞</button>
              <button>➤</button>
            </div>

          </div>
        ))}
      </div>

      <p className="clinicFooter">
        Can't find a clinic? Call your local emergency services.
      </p>

    </div>
  );
}
