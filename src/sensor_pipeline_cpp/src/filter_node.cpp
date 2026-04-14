#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/float64.hpp"

class FilterNode : public rclcpp::Node {
public:
    FilterNode()
    : Node("filter_node"),
      prev_filtered_(0.0),
      is_first_(true)
    {
        // 時定数（秒）
        this->declare_parameter("tau", 0.5);
        this->get_parameter("tau", tau_);

        sub_ = this->create_subscription<std_msgs::msg::Float64>(
            "/sensor/raw", 10,
            std::bind(&FilterNode::callback, this, std::placeholders::_1));

        pub_ = this->create_publisher<std_msgs::msg::Float64>(
            "/sensor/filtered", 10);

        last_time_ = this->now();

        RCLCPP_INFO(this->get_logger(),
            "Filter node started (tau=%.2f)", tau_);
    }

private:
    void callback(const std_msgs::msg::Float64::SharedPtr msg) {
        auto now = this->now();
        double dt = (now - last_time_).seconds();
        last_time_ = now;

        double raw = msg->data;
        double filtered;

        if (is_first_) {
            filtered = raw;
            prev_filtered_ = filtered;
            is_first_ = false;
            return;
        }

        // dtベースEMA
        double alpha = dt / (tau_ + dt);
        filtered = alpha * raw + (1.0 - alpha) * prev_filtered_;

        prev_filtered_ = filtered;

        std_msgs::msg::Float64 out_msg;
        out_msg.data = filtered;
        pub_->publish(out_msg);

        // デバッグログ
        RCLCPP_INFO(this->get_logger(),
            "dt=%.3f raw=%.3f filtered=%.3f",
            dt, raw, filtered);
    }

    double tau_;
    double prev_filtered_;
    bool is_first_;

    rclcpp::Time last_time_;

    rclcpp::Subscription<std_msgs::msg::Float64>::SharedPtr sub_;
    rclcpp::Publisher<std_msgs::msg::Float64>::SharedPtr pub_;
};

int main(int argc, char * argv[]) {
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<FilterNode>());
    rclcpp::shutdown();
    return 0;
}