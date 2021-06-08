<template>
  <div>
      <div class="bar-chart">
        <BarChart :data="barChartData" :options="{ maintainAspectRatio: false }" />
    </div>
  </div>
</template>

<script>
import BarChart from '@/components/singleProperty/bar-chart'

export default {
    components:
    BarChart,
    data() {
        return {
            barChartData: {
                  labels: ['A', 'B'],
                datasets: [
                    {
                        label: 'Nuxt.js Commit Activity',
                        backgroundColor: '#41b883',
                        data: 30,
                    }
                ]
            }
        }
    }
  }
 
</script>

<style>
.bar-chart {
  position: fixed;
  left: 10%;
  top: 10%;
  width: 80%;
  height: 80%;
}
</style>