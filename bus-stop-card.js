class BusStopCard extends HTMLElement {

  set hass(hass) {
    const entityId = this.config.entity;
    const state = hass.states[entityId];

    const stopNumber = entityId.split('_').pop();
    const stopName = this.config.stop_name || `Parada ${stopNumber}`;
    const lastRequestTime = state.attributes['last_request_time'];

    if (!this.content) {
      const card = document.createElement('ha-card');
      const header = document.createElement('div');
      header.classList.add('header-container');

      const stopNameElement = document.createElement('div');
      stopNameElement.textContent = stopName;

      const lastUpdateElement = document.createElement('div');
      lastUpdateElement.textContent = `Actualizado: ${lastRequestTime}`;
      lastUpdateElement.classList.add('last-update');

      header.appendChild(stopNameElement);
      header.appendChild(lastUpdateElement);
      card.appendChild(header);
      this.content = document.createElement('div');

      const style = document.createElement('style');
      style.textContent = `
      .header-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 6px 14px;
      }
      .last-update {
        font-size: 0.8em;
        color: #888;
        text-align: right;
      }
      table {
        width: 100%;
        padding: 6px 14px;
        border-spacing: 10px;
      }
      td {
        padding: 3px 0px;
      }
      td.shrink {
        white-space: nowrap;
      }
      td.expand {
        width: 99%;
      }
      span.line {
        font-weight: bold;
        font-size: 0.9em;
        padding: 3px 8px 2px 8px;
        color: #fff;
        background-color: #888;
        margin-right: 0.7em;
      }
      .route {
        font-style: italic;
        color: #555;
        padding-top: 5px;
      }
      `;
      card.appendChild(style);
      card.appendChild(this.content);
      this.appendChild(card);
    }

    let html = `<table>`;

    const arrivals = state.attributes['data'];
    if (Array.isArray(arrivals)) {
      for (const arrival of arrivals) {
        const title = arrival['title'];
        const nextArrivals = arrival['nextArrivals'];
        const longName = arrival['longName'];

        html += `<tr><td class="shrink"><span class="line">${title}</span></td>`;
        if (Array.isArray(nextArrivals)) {
          for (let i = 0; i < nextArrivals.length; i++) {
            html += `<td class="shrink" style="text-align:center;">${nextArrivals[i]}</td>`;
          }
        } else {
          html += `<td colspan="3">Sin información</td>`;
        }

        html += `</tr><tr><td class="route" colspan="4">${longName}</td></tr>`;

      }
    } else {
      html += `<tr><td colspan="4">No hay datos disponibles</td></tr>`;
    }

    html += `</table>`;

    this.content.innerHTML = html;
  }

  setConfig(config) {
    if (!config.entity) {
      throw new Error('You need to define an entity');
    }
    this.config = config;
  }

  getCardSize() {
    return 2;
  }
}

customElements.define('bus-stop-card', BusStopCard);
