import { check } from 'k6';
import http from 'k6/http';

export const options = {
  scenarios: {
    my_scenario1: {
      executor: 'constant-arrival-rate',
      duration: '30s', // durée totale du test
      preAllocatedVUs: 50, // pour allouer des ressources pendant l'exécution

      rate: 50, // nombre d'itérations constantes avec l'unité de temps spécifiée
      timeUnit: '1s',
    },
  },
};

export default function () {
  const url = 'https://iris-image-groupe7.proudforest-49e58823.francecentral.azurecontainerapps.io';
  const payload = JSON.stringify({
    features: [5.1, 3.5, 1.4, 0.2],
  });
  const headers = { 'Content-Type': 'application/json' };

  const res = http.post(url, payload, { headers });

  check(res, {
    'Post status is 200': (r) => r.status === 200,
    'Post Content-Type header': (r) => r.headers['Content-Type'] === 'application/json',
    'Post response features': (r) => r.status === 200,
  });
}
