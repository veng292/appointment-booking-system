// ==============================================================================
// Simple, Direct Booking Form Interactivity
// ==============================================================================

document.addEventListener("DOMContentLoaded", () => {
  const catSel       = document.getElementById("category");
  const svcSel       = document.getElementById("service_id");
  const dateSel      = document.getElementById("appointment_date");
  const timeInput    = document.getElementById("appointment_time");
  const slotsCont    = document.getElementById("slotsContainer");
  const detailsBox   = document.getElementById("serviceDetailsBox");
  const detailsText  = document.getElementById("serviceDetailsText");
  const form         = document.getElementById("bookingForm");
  const errBox       = document.getElementById("formError");
  const submitBtn    = document.getElementById("submitBtn");

  // 1. Filter services when category changes
  function filterServices() {
    const selectedCat = catSel.value;
    Array.from(svcSel.options).forEach(opt => {
      if (!opt.value) return; // Keep placeholder
      if (!selectedCat || opt.dataset.category === selectedCat) {
        opt.style.display = "";
      } else {
        opt.style.display = "none";
      }
    });

    // If current selected option is hidden, reset it
    const currOpt = svcSel.options[svcSel.selectedIndex];
    if (currOpt && currOpt.value && currOpt.style.display === "none") {
      svcSel.value = "";
      hideServiceDetails();
    }
  }

  function showServiceDetails(opt) {
    if (!opt || !opt.value) {
      hideServiceDetails();
      return;
    }
    detailsText.textContent = `Provider: ${opt.dataset.provider} (${opt.dataset.duration})`;
    detailsBox.classList.remove("hidden");
    
    // Auto sync category
    if (opt.dataset.category && catSel.value !== opt.dataset.category) {
      catSel.value = opt.dataset.category;
      filterServices();
    }
  }

  function hideServiceDetails() {
    detailsBox.classList.add("hidden");
    detailsText.textContent = "";
  }

  catSel.addEventListener("change", () => {
    filterServices();
    loadSlots();
  });

  svcSel.addEventListener("change", () => {
    showServiceDetails(svcSel.options[svcSel.selectedIndex]);
    loadSlots();
  });

  dateSel.addEventListener("change", loadSlots);

  // 2. Load available slots via API
  async function loadSlots() {
    timeInput.value = "";
    const sid = svcSel.value;
    const date = dateSel.value;

    if (!sid || !date) {
      slotsCont.innerHTML = `<p class="slots-helper-text">👉 Please select a Service and Date to view slots.</p>`;
      return;
    }

    slotsCont.innerHTML = `<p class="slots-helper-text">Loading available time slots...</p>`;

    try {
      const res = await fetch(`/api/slots?service_id=${encodeURIComponent(sid)}&date=${encodeURIComponent(date)}`);
      if (!res.ok) throw new Error("Failed to load slots");
      const data = await res.json();
      renderSlots(data.all_slots, data.booked);
    } catch (e) {
      slotsCont.innerHTML = `<p class="slots-helper-text" style="color:var(--error);">Failed to load slots. Please try again.</p>`;
    }
  }

  // 3. Render Slots cleanly
  function renderSlots(allSlots, bookedSlots) {
    if (!allSlots || !allSlots.length) {
      slotsCont.innerHTML = `<p class="slots-helper-text">No slots found for this date.</p>`;
      return;
    }

    const grid = document.createElement("div");
    grid.className = "slots-grid";

    allSlots.forEach(t => {
      const isBooked = bookedSlots.includes(t);
      const btn = document.createElement("button");
      btn.type = "button";
      btn.className = "slot-btn" + (isBooked ? " booked" : "");
      btn.textContent = t + (isBooked ? " (Booked)" : "");
      btn.dataset.time = t;

      if (!isBooked) {
        btn.addEventListener("click", () => {
          document.querySelectorAll(".slot-btn.selected").forEach(b => b.classList.remove("selected"));
          btn.classList.add("selected");
          timeInput.value = t;
          hideError();
        });
      }

      grid.appendChild(btn);
    });

    slotsCont.innerHTML = "";
    slotsCont.appendChild(grid);
  }

  // 4. Form Submit
  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    hideError();

    const name  = document.getElementById("customer_name").value.trim();
    const phone = document.getElementById("contact_number").value.trim();
    const sid   = svcSel.value;
    const date  = dateSel.value;
    const time  = timeInput.value;

    if (!sid)  return showError("Please select a Service.");
    if (!date) return showError("Please select an Appointment Date.");
    if (!time) return showError("Please select a Time Slot.");
    if (!name) return showError("Please enter your Full Name.");
    if (!/^\d{10}$/.test(phone)) return showError("Contact number must be exactly 10 digits.");

    submitBtn.disabled = true;
    submitBtn.textContent = "Booking Appointment...";

    try {
      const res = await fetch("/api/book", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          customer_name: name,
          contact_number: phone,
          service_id: sid,
          appointment_date: date,
          appointment_time: time
        })
      });

      const json = await res.json();
      if (json.success) {
        window.location.href = `/confirmation?booking_id=${json.booking.id}`;
      } else {
        showError(json.error || "Booking failed. Slot may have been taken.");
        loadSlots(); // Refresh slot availability
      }
    } catch (err) {
      showError("Network error. Please check your connection and try again.");
    } finally {
      submitBtn.disabled = false;
      submitBtn.textContent = "Confirm Appointment Booking →";
    }
  });

  function showError(msg) {
    errBox.textContent = msg;
    errBox.classList.remove("hidden");
  }

  function hideError() {
    errBox.classList.add("hidden");
  }

  // Initial Filter
  filterServices();
  if (svcSel.value) {
    showServiceDetails(svcSel.options[svcSel.selectedIndex]);
    loadSlots();
  }
});
