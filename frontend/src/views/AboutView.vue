<template>
  <div class="about-container">
    <n-card :title="homeText.about.title" class="about-card glass-effect">
      <div class="about-content">
        <div class="about-section">
          <h2>{{ homeText.about.mission.title }}</h2>
          <p>{{ homeText.about.mission.content }}</p>
        </div>
        
        <div class="about-section">
          <h2>{{ homeText.about.technology.title }}</h2>
          <div class="tech-grid">
            <div class="tech-item card-effect">
              <n-icon size="36" color="#2080f0">
                <InfoCircleIcon />
              </n-icon>
              <h3>{{ homeText.about.technology.dataAnalysis.title }}</h3>
              <p>{{ homeText.about.technology.dataAnalysis.content }}</p>
            </div>
            <div class="tech-item card-effect">
              <n-icon size="36" color="#18a058">
                <ShieldIcon />
              </n-icon>
              <h3>{{ homeText.about.technology.security.title }}</h3>
              <p>{{ homeText.about.technology.security.content }}</p>
            </div>
            <div class="tech-item card-effect">
              <n-icon size="36" color="#f0a020">
                <CheckCircleIcon />
              </n-icon>
              <h3>{{ homeText.about.technology.aiRecommendation.title }}</h3>
              <p>{{ homeText.about.technology.aiRecommendation.content }}</p>
            </div>
            <div class="tech-item card-effect">
              <n-icon size="36" color="#d03050">
                <TargetIcon />
              </n-icon>
              <h3>{{ homeText.about.technology.precision.title }}</h3>
              <p>{{ homeText.about.technology.precision.content }}</p>
            </div>
          </div>
        </div>
        
        <div class="about-section">
          <h2>{{ homeText.about.team.title }}</h2>
          <p>{{ homeText.about.team.content }}</p>
          <div class="team-info">
            <div class="team-stat blur-effect rounded-corner">
              <div class="stat-number">{{ homeText.about.team.stats.membersCount }}</div>
              <div class="stat-label">{{ homeText.about.team.members }}</div>
            </div>
            <div class="team-stat blur-effect rounded-corner">
              <div class="stat-number">{{ homeText.about.team.stats.experienceYears }}</div>
              <div class="stat-label">{{ homeText.about.team.experience }}</div>
            </div>
            <div class="team-stat blur-effect rounded-corner">
              <div class="stat-number">{{ homeText.about.team.stats.institutionsCount }}</div>
              <div class="stat-label">{{ homeText.about.team.institutions }}</div>
            </div>
          </div>
        </div>
        
        <div class="about-section">
          <h2>{{ homeText.about.contact.title }}</h2>
          <div class="contact-info">
            <div class="contact-item">
              <n-icon>
                <EmailIcon />
              </n-icon>
              <span>{{ homeText.about.contact.email }}</span>
            </div>
            <div class="contact-item">
              <n-icon>
                <PhoneIcon />
              </n-icon>
              <span>{{ homeText.about.contact.phone }}</span>
            </div>
            <div class="contact-item">
              <n-icon>
                <LocationIcon />
              </n-icon>
              <span>{{ homeText.about.contact.address }}</span>
            </div>
          </div>
        </div>
      </div>
    </n-card>
  </div>
</template>

<script setup lang="ts">
import { NCard, NIcon } from 'naive-ui'
import homeText from '../resource/home'
import { InfoCircleIcon, ShieldIcon, CheckCircleIcon, TargetIcon, EmailIcon, PhoneIcon, LocationIcon } from '../components/icons'
</script>

<style scoped>
.about-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 20px;
}

.about-card {
  margin-bottom: 20px;
}

.about-content {
  display: flex;
  flex-direction: column;
  gap: 40px;
}

.about-section {
  margin-bottom: 10px;
}

.about-section h2 {
  font-size: 1.8rem;
  color: #333;
  margin-bottom: 20px;
  position: relative;
  padding-bottom: 10px;
}

.about-section h2:after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 60px;
  height: 3px;
  background-color: #2080f0;
}

.tech-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 30px;
  margin-top: 30px;
}

.tech-item {
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  background-color: #fff;
  text-align: center;
  transition: transform 0.3s, box-shadow 0.3s;
}

.tech-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
}

.tech-item h3 {
  margin: 15px 0 10px;
  color: #333;
}

.tech-item p {
  font-size: 0.9rem;
  color: #666;
}

.team-info {
  display: flex;
  justify-content: space-around;
  margin-top: 30px;
  flex-wrap: wrap;
}

.team-stat {
  text-align: center;
  padding: 0 20px;
}

.stat-number {
  font-size: 2.5rem;
  font-weight: bold;
  color: #2080f0;
}

.stat-label {
  color: #666;
  margin-top: 5px;
}

.contact-info {
  margin-top: 20px;
  display: flex;
  flex-direction: column;
  gap: 15px;
}

.contact-item {
  display: flex;
  align-items: center;
  gap: 10px;
}

.contact-item span {
  color: #333;
}
</style>