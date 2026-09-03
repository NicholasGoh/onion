import http from "k6/http";
import { check, sleep } from "k6";

const BASE_URL = __ENV.BASE_URL || "http://localhost:8000";
// Kratos session token, sent as X-Session-Token on every request - all
// routes require authn at the router level (see api/app/main.py). Without
// it every request 401s (see the expectStatus checks below).
const SESSION_TOKEN = __ENV.SESSION_TOKEN || "";
const expectStatus = SESSION_TOKEN ? 200 : 401;

export const options = {
  scenarios: {
    smoke: {
      executor: "constant-vus",
      vus: 5,
      duration: "5s",
    },
  },
  thresholds: {
    http_req_duration: ["p(95)<500"],
  },
};

function jsonHeaders(extra) {
  return {
    headers: {
      "Content-Type": "application/json",
      ...(SESSION_TOKEN ? { "X-Session-Token": SESSION_TOKEN } : {}),
      ...extra,
    },
  };
}

export default function () {
  const item = http.post(
    `${BASE_URL}/items/`,
    JSON.stringify({ name: `item-${__VU}-${__ITER}`, description: "load test item" }),
    jsonHeaders(),
  );
  check(item, { [`create item ${expectStatus}`]: (r) => r.status === expectStatus });
  const itemId = expectStatus === 200 ? item.json("id") : null;

  check(http.get(`${BASE_URL}/items/`, jsonHeaders()), { [`list items ${expectStatus}`]: (r) => r.status === expectStatus });
  check(http.get(`${BASE_URL}/items/search?q=item`, jsonHeaders()), { [`search items ${expectStatus}`]: (r) => r.status === expectStatus });

  if (itemId) {
    check(http.get(`${BASE_URL}/items/${itemId}`, jsonHeaders()), { "get item 200": (r) => r.status === 200 });
  }

  const tag = http.post(
    `${BASE_URL}/tags/`,
    JSON.stringify({ name: `tag-${__VU}-${__ITER}` }),
    jsonHeaders(),
  );
  check(tag, { [`create tag ${expectStatus}`]: (r) => r.status === expectStatus });

  check(http.get(`${BASE_URL}/tags/`, jsonHeaders()), { [`list tags ${expectStatus}`]: (r) => r.status === expectStatus });

  if (itemId) {
    const order = http.post(
      `${BASE_URL}/orders/`,
      JSON.stringify({ itemIds: [itemId], quantity: { [itemId]: 1 } }),
      jsonHeaders(),
    );
    check(order, { "create order 200": (r) => r.status === 200 });
    const orderId = order.json("id");
    if (orderId) {
      check(http.get(`${BASE_URL}/orders/${orderId}`, jsonHeaders()), { "get order 200": (r) => r.status === 200 });
    }

    const quote = http.post(
      `${BASE_URL}/orders/quote`,
      JSON.stringify({ itemIds: [itemId], quantity: { [itemId]: 1 } }),
      jsonHeaders(),
    );
    check(quote, { [`quote order ${expectStatus}`]: (r) => r.status === expectStatus });
  }

  check(http.get(`${BASE_URL}/orders/`, jsonHeaders()), { [`list orders ${expectStatus}`]: (r) => r.status === expectStatus });

  sleep(1);
}
