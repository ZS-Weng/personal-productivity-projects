// Pomodoro Timer JavaScript
class PomodoroTimer {
    constructor() {
        this.timerMinutes = 25;
        this.timeLeft = this.timerMinutes * 60;
        this.isRunning = false;
        this.timerInterval = null;
        this.pomodoroCount = 0;

        this.initializeElements();
        this.setupEventListeners();
        this.loadStats();
        this.loadAvailableYears();
        this.updateDisplay();
    }

    initializeElements() {
        // Timer elements
        this.timeDisplay = document.getElementById('timeDisplay');
        this.progressCircle = document.getElementById('progressCircle');
        this.timerMinutesInput = document.getElementById('timerMinutes');

        // Control buttons
        this.startBtn = document.getElementById('startBtn');
        this.pauseBtn = document.getElementById('pauseBtn');
        this.resetBtn = document.getElementById('resetBtn');
        this.saveBtn = document.getElementById('saveBtn');

        // Counter
        this.pomodoroCounter = document.getElementById('pomodoroCounter');

        // Stats elements
        this.yearFilter = document.getElementById('yearFilter');
        this.monthFilter = document.getElementById('monthFilter');
        this.filterBtn = document.getElementById('filterBtn');
        this.totalPomodoros = document.getElementById('totalPomodoros');
        this.totalSessions = document.getElementById('totalSessions');
        this.monthlyBreakdown = document.getElementById('monthlyBreakdown');
    }

    setupEventListeners() {
        this.startBtn.addEventListener('click', () => this.startTimer());
        this.pauseBtn.addEventListener('click', () => this.pauseTimer());
        this.resetBtn.addEventListener('click', () => this.resetTimer());
        this.saveBtn.addEventListener('click', () => this.saveSession());
        this.timerMinutesInput.addEventListener('change', () => this.changeTimerMinutes());
        this.filterBtn.addEventListener('click', () => this.loadStats());
    }

    changeTimerMinutes() {
        let minutes = parseInt(this.timerMinutesInput.value, 10);
        if (isNaN(minutes) || minutes < 1) minutes = 1;
        if (minutes > 60) minutes = 60;
        this.timerMinutes = minutes;
        this.resetTimer();
    }

    startTimer() {
        if (this.isRunning) return;
        this.isRunning = true;
        this.startBtn.disabled = true;
        this.pauseBtn.disabled = false;
        this.timerMinutesInput.disabled = true;

        this.timerInterval = setInterval(() => {
            if (this.timeLeft > 0) {
                this.timeLeft--;
                this.updateDisplay();
            } else {
                this.completePomodoro();
            }
        }, 1000);
    }

    pauseTimer() {
        if (!this.isRunning) return;
        this.isRunning = false;
        clearInterval(this.timerInterval);
        this.startBtn.disabled = false;
        this.pauseBtn.disabled = true;
    }

    resetTimer() {
        this.isRunning = false;
        clearInterval(this.timerInterval);
        this.timeLeft = this.timerMinutes * 60;
        this.updateDisplay();
        this.startBtn.disabled = false;
        this.pauseBtn.disabled = true;
        this.timerMinutesInput.disabled = false;
    }

    completePomodoro() {
        this.pomodoroCount++;
        this.pomodoroCounter.textContent = this.pomodoroCount;
        this.saveBtn.disabled = false;
        this.resetTimer();
        // Optionally, play a sound or show a notification here
    }

    updateDisplay() {
        // Update time
        const minutes = Math.floor(this.timeLeft / 60).toString().padStart(2, '0');
        const seconds = (this.timeLeft % 60).toString().padStart(2, '0');
        this.timeDisplay.textContent = `${minutes}:${seconds}`;

        // Update progress circle
        const total = this.timerMinutes * 60;
        const percent = 1 - (this.timeLeft / total);
        const circleLength = 2 * Math.PI * 90; // r=90
        this.progressCircle.setAttribute('stroke-dashoffset', (1 - percent) * circleLength);

        // Update counter
        this.pomodoroCounter.textContent = this.pomodoroCount;
    }

    async saveSession() {
        this.saveBtn.disabled = true;
        const year = this.yearFilter.value || new Date().getFullYear();
        const month = this.monthFilter.value || (new Date().getMonth() + 1);
        try {
            const response = await fetch('/api/save-pomodoros', {
                method: 'POST',
                headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
                body: `pomodoros=${this.pomodoroCount}&year=${year}&month=${month}`
            });
            const data = await response.json();
            if (data.success) {
                alert(data.message);
                this.pomodoroCount = 0;
                this.pomodoroCounter.textContent = this.pomodoroCount;
                this.loadStats();
            } else {
                alert('Failed to save session.');
            }
        } catch (err) {
            alert('Error saving session.');
        }
    }

    async loadStats() {
        let url = '/api/stats';
        const year = this.yearFilter.value;
        const month = this.monthFilter.value;
        const params = [];
        if (year) params.push(`year=${year}`);
        if (month) params.push(`month=${month}`);
        if (params.length) url += '?' + params.join('&');

        try {
            const response = await fetch(url);
            const data = await response.json();
            this.totalPomodoros.textContent = data.total_pomodoros;
            this.totalSessions.textContent = data.total_sessions;
            this.renderMonthlyBreakdown(data.monthly_breakdown || []);
        } catch (err) {
            this.totalPomodoros.textContent = '0';
            this.totalSessions.textContent = '0';
            this.monthlyBreakdown.innerHTML = '';
        }
    }

    renderMonthlyBreakdown(breakdown) {
        if (!breakdown.length) {
            this.monthlyBreakdown.innerHTML = '<p>No monthly data available.</p>';
            return;
        }
        let html = '<table><tr><th>Month</th><th>Pomodoros</th></tr>';
        breakdown.forEach(item => {
            html += `<tr><td>${this.getMonthName(item.month)}</td><td>${item.total}</td></tr>`;
        });
        html += '</table>';
        this.monthlyBreakdown.innerHTML = html;
    }

    getMonthName(month) {
        const months = [
            '', 'January', 'February', 'March', 'April', 'May', 'June',
            'July', 'August', 'September', 'October', 'November', 'December'
        ];
        return months[month] || month;
    }

    async loadAvailableYears() {
        try {
            const response = await fetch('/api/years');
            const data = await response.json();
            this.yearFilter.innerHTML = '<option value="">All Years</option>';
            const years = new Set(data.years);
            years.add(2025); // Always include 2025
            Array.from(years).sort().forEach(year => {
                const opt = document.createElement('option');
                opt.value = year;
                opt.textContent = year;
                this.yearFilter.appendChild(opt);
            });
        } catch (err) {
            this.yearFilter.innerHTML = '<option value="">All Years</option><option value="2025">2025</option>';
        }
    }
}

// Initialize when DOM is ready
window.addEventListener('DOMContentLoaded', () => {
    new PomodoroTimer();
});