document.addEventListener('DOMContentLoaded', () => {
    fetch('match_output.json')
      .then(response => response.json())
      .then(data => displayAllMatchData(data))
      .catch(error => console.error('Error loading match data:', error));
  });
  
  function displayAllMatchData(data) {
    const matchInfoDiv = document.getElementById('match-info');
  
    // Fixture and general information
    let content = `
      <h2>Fixture: ${data.fixture[0]} vs. ${data.fixture[1]}</h2>
      <p>Stadium: ${data.stadium}</p>
      <p>Weather: ${data.weather}</p>
      <p>Pitch Condition: ${data.pitch_condition}</p>
      <p>Match Type: ${data.type_of_match}</p>
      <h3>Referee Information</h3>
      <p>Name: ${data.referee.name}</p>
      <p>Fouls per Tackle: ${data.referee.fouls_per_tackle}</p>
      <p>Yellow Cards per Game: ${data.referee.yellow_per_game}</p>
    `;
  
    // Head-to-head information
    content += `<h3>Head-to-Head Matches</h3>`;
    Object.entries(data.head_to_head.teams).forEach(([match, teams]) => {
      const goals = data.head_to_head.goals[match];
      const xGoals = data.head_to_head.x_goals[match];
      const corners = data.head_to_head.corners[match];
      const fouls = data.head_to_head.fouls[match];
  
      content += `
        <div class="match-block">
          <h4>${teams[0]} vs. ${teams[1]}</h4>
          <p>Goals: ${goals[0]} - ${goals[1]}</p>
          <p>xG: ${xGoals[0]} - ${xGoals[1]}</p>
          <p>Corners: ${corners[0]} - ${corners[1]}</p>
          <p>Fouls: ${fouls[0]} - ${fouls[1]}</p>
        </div>
      `;
    });
  
    // Insert the content into the div
    matchInfoDiv.innerHTML = content;
  }
  