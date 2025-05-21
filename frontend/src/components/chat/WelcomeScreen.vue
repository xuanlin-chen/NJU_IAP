<template>
  <div class="welcome-container">
    <h1>{{ chatResource.title }}</h1>
    <p>{{ chatResource.welcomeMessage }}</p>
    
    <div class="examples-container">
      <h3>{{ chatResource.examples.title }}</h3>
      <transition-group name="example" tag="div" class="examples-grid">
        <div 
          v-for="(example, index) in chatResource.examples.questions" 
          :key="index" 
          class="example-item"
          @click="$emit('ask-example', example)"
          :style="{ animationDelay: index * 0.1 + 's' }"
        >
          {{ example }}
        </div>
      </transition-group>
    </div>
  </div>
</template>

<script setup lang="ts">
import chatResource from '../../resource/chat'

defineEmits(['ask-example'])
</script>

<style scoped>
.welcome-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  text-align: center;
  padding: 20px;
}

.welcome-container h1 {
  font-size: 32px;
  margin-bottom: 16px;
  color: #333;
  animation: slide-down 0.5s ease;
}

.welcome-container p {
  font-size: 16px;
  color: #666;
  max-width: 600px;
  margin-bottom: 40px;
  animation: slide-down 0.5s ease 0.1s both;
}

.examples-container {
  max-width: 800px;
  width: 100%;
}

.examples-container h3 {
  margin-bottom: 20px;
  color: #666;
  animation: slide-down 0.5s ease 0.2s both;
}

.examples-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 16px;
}

.example-item {
  padding: 16px;
  background-color: #f9f9fb;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  cursor: pointer;
  transition: transform 0.2s, background-color 0.2s, box-shadow 0.2s;
  animation: fade-in 0.5s ease both;
}

.example-item:hover {
  background-color: #f0f0f0;
  transform: translateY(-3px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

/* 示例项目的过渡效果 */
.example-enter-active,
.example-leave-active {
  transition: all 0.4s ease;
}

.example-enter-from,
.example-leave-to {
  opacity: 0;
  transform: translateY(30px);
}

.example-move {
  transition: transform 0.4s ease;
}

@keyframes slide-down {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes fade-in {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
</style>