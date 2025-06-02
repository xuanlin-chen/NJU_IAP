<template>
  <div class="about-container">
    <n-card :title="homeText.about.title" class="about-card glass-effect">
      <div class="about-content">
        <div class="about-section">
          <h2>{{ homeText.about.mission.title }}</h2>
          <div class="mission-block">
            <p>{{ homeText.about.mission.content_1 }}</p>
            <h4>{{ homeText.about.mission.content_2 }}</h4>
            <p>{{ homeText.about.mission.content_3 }}</p>
            <p>{{ homeText.about.mission.content_4 }}</p>
            <p>{{ homeText.about.mission.content_5 }}</p>
            <p>{{ homeText.about.mission.content_6 }}</p>
            <h4>{{ homeText.about.mission.content_7 }}</h4>
            <p>{{ homeText.about.mission.content_8 }}</p>
            <p>{{ homeText.about.mission.content_9 }}</p>
            <p>{{ homeText.about.mission.content_10 }}</p>
            <p>{{ homeText.about.mission.content_11 }}</p>
          </div>
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
          <div class="team-content">
            <p>{{ homeText.about.team.content }}</p>
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
                <LocationIcon />
              </n-icon>
              <a :href="homeText.about.contact.address" target="_blank">{{ homeText.about.contact.address }}</a>
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
import { InfoCircleIcon, ShieldIcon, CheckCircleIcon, TargetIcon, EmailIcon, LocationIcon } from '../components/icons'
</script>

<style scoped>
.about-container {
  max-width: 1000px;
  margin: 0 auto;
  padding: 40px 20px;
  min-height: 100vh;
  background: linear-gradient(135deg, rgba(255,255,255,0.9), rgba(255,255,255,0.7));
}

.about-card {
  margin-bottom: 30px;
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 8px 32px rgba(31, 38, 135, 0.15);
  transition: transform 0.3s ease;
}

.about-card:hover {
  transform: translateY(-5px);
}

.about-section {
  margin-bottom: 50px;
  animation: fadeInUp 0.6s ease-out;
}

.about-section h2 {
  font-size: 2rem;
  color: #2c3e50;
  margin-bottom: 30px;
  position: relative;
  padding-bottom: 15px;
  font-weight: 600;
}

.about-section h2:after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 80px;
  height: 4px;
  background: linear-gradient(90deg, #2080f0, #42b883);
  border-radius: 2px;
}

.tech-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 30px;
  margin-top: 30px;
}

/* 响应式布局调整 */
@media (min-width: 1200px) {
  .tech-grid {
    grid-template-columns: repeat(4, 1fr);
  }
}

@media (max-width: 768px) {
  .tech-grid {
    grid-template-columns: 1fr;
  }
}
.tech-item {
  padding: 30px;
  border-radius: 16px;
  background: rgba(255, 255, 255, 0.9);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  text-align: center;
  transition: all 0.4s ease;
  border: 1px solid rgba(255, 255, 255, 0.2);
}

.tech-item:hover {
  transform: translateY(-8px);
  box-shadow: 0 12px 28px rgba(0, 0, 0, 0.12);
  background: rgba(255, 255, 255, 0.95);
}

.tech-item h3 {
  margin: 20px 0 15px;
  color: #2c3e50;
  font-size: 1.4rem;
  font-weight: 600;
}

.tech-item p {
  font-size: 1rem;
  color: #5c6c7c;
  line-height: 1.6;
  margin-bottom: 15px;
}

.mission-block {
  background: rgba(255, 255, 255, 0.9);
  padding: 25px;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
  margin: 20px 0;
}

.mission-block h4 {
  color: #2c3e50;
  font-size: 1.2rem;
  margin: 20px 0 15px;
  font-weight: 600;
}

.mission-block p {
  margin-bottom: 12px;
}

.team-content {
  background: rgba(255, 255, 255, 0.9);
  padding: 25px;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
  margin: 20px 0;
}

.contact-info {
  margin-top: 30px;
  display: flex;
  flex-direction: column;
  gap: 20px;
  background: rgba(255, 255, 255, 0.8);
  padding: 25px;
  border-radius: 12px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
}

.contact-item {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 10px;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.contact-item:hover {
  background: rgba(32, 128, 240, 0.1);
  transform: translateX(5px);
}

.contact-item span, .contact-item a {
  color: #2c3e50;
  font-size: 1.1rem;
  text-decoration: none;
  transition: color 0.3s ease;
}

.contact-item a:hover {
  color: #2080f0;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

/* 响应式优化 */
@media (max-width: 768px) {
  .about-container {
    padding: 20px 15px;
  }
  
  .tech-grid {
    grid-template-columns: 1fr;
    gap: 25px;
  }
  
  .about-section h2 {
    font-size: 1.6rem;
  }
  
  .tech-item {
    padding: 20px;
  }
}
</style>
